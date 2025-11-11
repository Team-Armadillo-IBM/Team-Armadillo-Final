"""Simple helper functions for normalizing banking risk metrics into a 0-1 score."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass
class RiskFactors:
    """Container describing the primary drivers that influence the risk score."""

    delinquency_rate: float
    collateral_ratio: float
    portfolio_concentration: float

    def as_array(self) -> np.ndarray:
        return np.array(
            [self.delinquency_rate, self.collateral_ratio, self.portfolio_concentration],
            dtype=float,
        )


DEFAULT_WEIGHTS = np.array([0.5, 0.3, 0.2], dtype=float)


def _validate_inputs(values: Iterable[float]) -> np.ndarray:
    arr = np.asarray(list(values), dtype=float)
    if arr.shape != (3,):
        raise ValueError("Expected three input factors: delinquency_rate, collateral_ratio, portfolio_concentration.")
    if np.any(arr < 0) or np.any(arr > 1):
        raise ValueError("Each risk factor must be normalized to the range [0, 1].")
    return arr


def calculate_risk_score(
    delinquency_rate: float,
    collateral_ratio: float,
    portfolio_concentration: float,
    weights: Iterable[float] | None = None,
) -> float:
    """Compute a weighted risk score between 0 and 1 for the provided factors."""
    factors = _validate_inputs((delinquency_rate, collateral_ratio, portfolio_concentration))
    weights_arr = np.asarray(list(weights) if weights is not None else DEFAULT_WEIGHTS, dtype=float)

    if weights_arr.shape != (3,):
        raise ValueError("Weights array must contain exactly three elements.")

    weights_arr = weights_arr / weights_arr.sum()
    score = float(np.clip(np.dot(factors, weights_arr), 0.0, 1.0))
    return score


__all__ = ["RiskFactors", "calculate_risk_score"]
