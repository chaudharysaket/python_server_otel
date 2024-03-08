from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
import logging

# Set common resource
resource = Resource(attributes={"service.name": "your-service-name"})

# Configure standard Python logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure tracing
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)
otlp_span_exporter = OTLPSpanExporter(endpoint="http://127.0.0.1:4317", insecure=True)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_span_exporter)
)

# Configure metrics
metrics.set_meter_provider(MeterProvider(resource=resource))
meter = metrics.get_meter(__name__, version="0.1")
otlp_metric_exporter = OTLPMetricExporter(endpoint="http://127.0.0.1:4317", insecure=True)
metric_reader = PeriodicExportingMetricReader(otlp_metric_exporter)
# metrics.get_meter_provider().register_metric_reader(metric_reader)

# Create a span
with tracer.start_as_current_span("example-span"):
    logger.info("Hello, OpenTelemetry Traces!")

# Create and record a metric
counter = meter.create_counter(
    "example-counter",
    description="An example counter",
    unit="1"
)
counter.add(1, {"method": "repl"})
