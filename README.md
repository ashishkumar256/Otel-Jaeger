helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
helm show values jaegertracing/jaeger

helm upgrade --install jaeger jaegertracing/jaeger \
     --namespace devops \
     --create-namespace \
     --history-max 3 \
     --version 3.3.3 \
     --values jaeger.yaml

helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm upgrade --install otel-collector open-telemetry/opentelemetry-collector \
     --namespace devops \
     --create-namespace \
     --version 0.111.1 \
     --values otel-collector.yaml \
     --set image.repository="otel/opentelemetry-collector-k8s"
