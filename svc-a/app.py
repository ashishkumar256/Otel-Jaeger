from flask import Flask, jsonify
import os, requests

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

resource = Resource.create(attributes={
    ResourceAttributes.SERVICE_NAME: "service-a", # or "service-b" for the other service
})

app = Flask(__name__)
tracer = trace.get_tracer(__name__)

# Initialize OpenTelemetry tracing
# trace.set_tracer_provider(TracerProvider())
trace.set_tracer_provider(TracerProvider(resource=resource))

span_exporter = OTLPSpanExporter(endpoint=os.environ['OTEL_ENDPOINT'], insecure=True)
span_processor = BatchSpanProcessor(span_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

# Enable OpenTelemetry middleware for WSGI
app.wsgi_app = OpenTelemetryMiddleware(app.wsgi_app)

@app.route('/call-service-b')
def call_service_b():
    with tracer.start_as_current_span("calling service-b"):
        # Use the Kubernetes service name to communicate with service-b
        service_b_response = requests.get("http://service-b.devops.svc.cluster.local:5000/complex-operation")
        return jsonify(service_b_response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
