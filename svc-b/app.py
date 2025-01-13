import os
from flask import Flask, jsonify
from time import sleep

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

resource = Resource.create(attributes={
    ResourceAttributes.SERVICE_NAME: "service-b", # or "service-b" for the other service
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

# Enable OpenTelemetry middleware for WSGI
app.wsgi_app = OpenTelemetryMiddleware(app.wsgi_app)

@app.route('/complex-operation')
def complex_operation():
    with tracer.start_as_current_span("complex operation"):
        # Simulate a complex operation with some processing time
        for _ in range(5):
            with tracer.start_as_current_span("step"):
                sleep(0.1)  # Simulating a processing step
    return jsonify({"result": "Complex operation completed"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
