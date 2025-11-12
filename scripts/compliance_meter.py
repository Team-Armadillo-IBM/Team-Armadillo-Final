"""Utilities for rendering a compliance health meter visualization."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import matplotlib.pyplot as plt
import pandas as pd


@dataclass(frozen=True)
class ComplianceHealth:
    """Summary of the compliance risk posture."""

    average_risk: float
    color: str
    status: str


_STATUS_BANDS: Sequence[tuple[float, float, str, str]] = (
    (0.0, 0.33, "green", "🟢 LOW RISK — Policies appear compliant and stable."),
    (0.33, 0.66, "gold", "🟡 MODERATE RISK — Review flagged sections or outliers."),
    (0.66, 1.0, "red", "🔴 HIGH RISK — Policy misalignment or potential compliance gap detected."),
)


def _determine_status(avg_risk: float) -> ComplianceHealth:
    """Return the compliance status metadata for the provided average risk."""

    for lower, upper, color, status in _STATUS_BANDS:
        if lower <= avg_risk < upper:
            return ComplianceHealth(avg_risk, color, status)
    # avg_risk could be exactly 1.0 after rounding
    return ComplianceHealth(avg_risk, "red", _STATUS_BANDS[-1][3])


def _coerce_dataframe(records: Iterable[dict] | pd.DataFrame, risk_column: str) -> pd.DataFrame:
    if isinstance(records, pd.DataFrame):
        df = records.copy()
    else:
        df = pd.DataFrame.from_records(records)

    if risk_column not in df.columns:
        raise KeyError(f"Missing '{risk_column}' column required to compute risk averages.")

    df = df[[risk_column]].dropna()
    if df.empty:
        raise ValueError("No records with valid risk scores were provided.")

    df[risk_column] = df[risk_column].astype(float)
    if (df[risk_column] < 0).any() or (df[risk_column] > 1).any():
        raise ValueError("Risk scores must be normalized in the range [0, 1].")

    return df


def render_compliance_health_meter(
    records: Iterable[dict] | pd.DataFrame,
    risk_column: str = "risk_score",
    ax: plt.Axes | None = None,
) -> ComplianceHealth:
    """Render a horizontal compliance health meter bar chart.

    Parameters
    ----------
    records:
        Iterable of governance log dictionaries or a pandas DataFrame containing risk
        scores. Each record must expose the value under ``risk_column``.
    risk_column:
        Name of the column that stores the risk score values.
    ax:
        Optional matplotlib axes on which to render the chart. When omitted, a new
        ``Figure`` and ``Axes`` will be created. The figure is returned implicitly via
        ``ax.figure``.

    Returns
    -------
    ComplianceHealth
        Dataclass containing the average risk, associated color, and descriptive
        status string.
    """

    df = _coerce_dataframe(records, risk_column)
    avg_risk = float(df[risk_column].mean())

    health = _determine_status(avg_risk)

    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 1.2))
    else:
        fig = ax.figure
        ax.clear()

    ax.barh(["Compliance"], [health.average_risk], color=health.color, height=0.3)
    ax.set_xlim(0, 1)
    ax.set_xlabel("Average Risk (0–1)", fontsize=10)
    ax.set_title("⚖️ Compliance Health Meter", fontsize=12)
    ax.set_yticks([])
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])

    fig.tight_layout()

    return health


__all__ = ["ComplianceHealth", "render_compliance_health_meter"]
