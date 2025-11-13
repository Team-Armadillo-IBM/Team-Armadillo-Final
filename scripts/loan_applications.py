"""Utility helpers for loading structured loan application datasets."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

import yaml


@dataclass(frozen=True)
class LoanApplication:
    """Structured view of a single loan application record."""

    applicant_id: int
    risk_score: float
    credit_score: int
    debt_to_income: float
    explanation: str
    risk_tier: str

    def as_dict(self) -> dict[str, str | float | int]:
        """Return the application data as a JSON-serializable dictionary."""

        return {
            "applicant_id": self.applicant_id,
            "risk_score": self.risk_score,
            "credit_score": self.credit_score,
            "debt_to_income": self.debt_to_income,
            "explanation": self.explanation,
            "risk_tier": self.risk_tier,
        }

    @classmethod
    def from_mapping(cls, tier: str, payload: Mapping[str, object]) -> "LoanApplication":
        """Validate and coerce a YAML mapping into a ``LoanApplication`` instance."""

        required_fields = {"applicant_id", "risk_score", "credit_score", "debt_to_income", "explanation"}
        missing = required_fields - payload.keys()
        if missing:
            missing_fields = ", ".join(sorted(missing))
            raise KeyError(f"Missing required field(s) for tier '{tier}': {missing_fields}")

        return cls(
            applicant_id=int(payload["applicant_id"]),
            risk_score=float(payload["risk_score"]),
            credit_score=int(payload["credit_score"]),
            debt_to_income=float(payload["debt_to_income"]),
            explanation=str(payload["explanation"]),
            risk_tier=tier,
        )


def load_loan_applications(path: str | Path) -> list[LoanApplication]:
    """Load loan application records from a YAML file keyed by risk tier."""

    path_obj = Path(path)
    if not path_obj.exists():
        raise FileNotFoundError(f"Loan application file not found: {path_obj}")

    contents = path_obj.read_text(encoding="utf-8")
    data = yaml.safe_load(contents) or {}
    if not isinstance(data, Mapping):
        raise ValueError("Loan application payload must be a mapping of risk tiers to records.")

    applications: list[LoanApplication] = []
    for tier, payload in data.items():
        if not isinstance(payload, Mapping):
            raise ValueError(f"Expected mapping for tier '{tier}', received {type(payload)!r}.")
        applications.append(LoanApplication.from_mapping(str(tier), payload))

    return applications


def summarize_by_tier(applications: Iterable[LoanApplication]) -> dict[str, list[LoanApplication]]:
    """Group loan applications by their risk tier label."""

    grouped: dict[str, list[LoanApplication]] = {}
    for application in applications:
        grouped.setdefault(application.risk_tier, []).append(application)
    return grouped


__all__ = ["LoanApplication", "load_loan_applications", "summarize_by_tier"]
