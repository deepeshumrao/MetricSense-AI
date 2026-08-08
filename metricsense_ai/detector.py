"""Anomaly detection primitives for tabular metric rows."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, median, pstdev
from typing import Any, Iterable


@dataclass(frozen=True)
class AnomalyResult:
    """Detection result for one row."""

    index: int
    value: float
    score: float
    is_anomaly: bool
    row: dict[str, Any]


def detect_anomalies(
    rows: Iterable[dict[str, Any]],
    value_column: str | None = None,
    threshold: float = 3.0,
    method: str = "robust",
) -> list[AnomalyResult]:
    """Detect unusual numeric values in rows.

    The default robust method uses median absolute deviation, which handles
    occasional spikes better than a plain standard deviation score.
    """

    materialized_rows = list(rows)
    if not materialized_rows:
        return []

    selected_column = value_column or infer_numeric_column(materialized_rows)
    values: list[tuple[int, float]] = []

    for index, row in enumerate(materialized_rows):
        value = coerce_float(row.get(selected_column))
        if value is not None:
            values.append((index, value))

    if not values:
        raise ValueError(f"No numeric values found in column '{selected_column}'.")

    if method not in {"robust", "zscore"}:
        raise ValueError("method must be 'robust' or 'zscore'.")

    numeric_values = [value for _, value in values]
    scores = _robust_scores(numeric_values) if method == "robust" else _z_scores(numeric_values)

    results: list[AnomalyResult] = []
    for (row_index, value), score in zip(values, scores):
        results.append(
            AnomalyResult(
                index=row_index,
                value=value,
                score=score,
                is_anomaly=abs(score) >= threshold,
                row=materialized_rows[row_index],
            )
        )

    return results


def infer_numeric_column(rows: list[dict[str, Any]]) -> str:
    """Return the first column that contains at least one numeric value."""

    for key in rows[0].keys():
        if any(coerce_float(row.get(key)) is not None for row in rows):
            return key
    raise ValueError("No numeric column could be inferred.")


def coerce_float(value: Any) -> float | None:
    """Convert common spreadsheet values to float."""

    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        normalized = value.strip().replace(",", "")
        if normalized == "":
            return None
        try:
            return float(normalized)
        except ValueError:
            return None
    return None


def _robust_scores(values: list[float]) -> list[float]:
    center = median(values)
    deviations = [abs(value - center) for value in values]
    mad = median(deviations)

    if mad == 0:
        return _z_scores(values)

    return [0.6745 * (value - center) / mad for value in values]


def _z_scores(values: list[float]) -> list[float]:
    if len(values) == 1:
        return [0.0]

    center = mean(values)
    deviation = pstdev(values)
    if deviation == 0:
        return [0.0 for _ in values]

    return [(value - center) / deviation for value in values]
