"""Uptrace exporter for OpenTelemetry"""

from .uptrace import configure_opentelemetry, shutdown, report_exception, trace_url
from .version import __version__
from .dsn import parse_dsn

__all__ = [
    "configure_opentelemetry",
    "shutdown",
    "trace_url",
    "report_exception",
    "parse_dsn",
    "__version__",
]
