"""MetricSense AI package."""

from .detector import AnomalyResult, detect_anomalies
from .io import load_table, write_anomaly_report

__all__ = [
    "AnomalyResult",
    "detect_anomalies",
    "load_table",
    "write_anomaly_report",
]

__version__ = "0.1.0"
