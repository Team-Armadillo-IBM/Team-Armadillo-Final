"""Configuration objects for building Agent Lab agents."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional


@dataclass(frozen=True)
class Credentials:
    """Authentication credentials for watsonx.ai services."""

    url: str
    api_key: str


@dataclass(frozen=True)
class Workspace:
    """Execution context metadata used by watsonx.ai."""

    project_id: Optional[str] = None
    space_id: Optional[str] = None

    def as_kwargs(self) -> Dict[str, str]:
        """Return keyword arguments for API client construction."""
        data: Dict[str, str] = {}
        if self.project_id:
            data["project_id"] = self.project_id
        if self.space_id:
            data["space_id"] = self.space_id
        return data


@dataclass(frozen=True)
class ModelParameters:
    """Tunable inference parameters for Granite chat models."""

    frequency_penalty: float = 0
    max_tokens: int = 2000
    presence_penalty: float = 0
    temperature: float = 0
    top_p: float = 1

    def as_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation consumable by the SDK."""
        return {
            "frequency_penalty": self.frequency_penalty,
            "max_tokens": self.max_tokens,
            "presence_penalty": self.presence_penalty,
            "temperature": self.temperature,
            "top_p": self.top_p,
        }


@dataclass(frozen=True)
class ModelConfig:
    """Model selection configuration."""

    model_id: str = "ibm/granite-3-3-8b-instruct"
    parameters: ModelParameters = field(default_factory=ModelParameters)


@dataclass(frozen=True)
class RagToolConfig:
    """Configuration for retrieving knowledge-grounded context."""

    vector_index_id: str
    description: str = (
        "Search information in documents to provide context to a user query. "
        "Useful when asked to ground the answer in specific knowledge about Mock Bank Policy Global"
    )


@dataclass(frozen=True)
class CustomToolConfig:
    """Definition for dynamically compiled custom tools."""

    name: str
    description: str
    code: str
    schema: Mapping[str, Any]
    params: Optional[Mapping[str, Any]] = None


@dataclass(frozen=True)
class AgentInstructions:
    """Textual guidelines for the agent's behaviour."""

    instructions: str


DEFAULT_INSTRUCTIONS = AgentInstructions(
    instructions="""# Notes
- When a tool is required to answer the user's query, respond only with <|tool_call|> followed by a JSON list of tools used.
- If a tool does not exist in the provided list of tools, notify the user that you do not have the ability to fulfill the request.
You are Loan Risk Assistant, an enterprise AI agent for evaluating loan applications
according to documented bank policies.

## Purpose
Assess risk, cite relevant policy rules, and produce a JSON report suitable for
watsonx.governance logging.

## Responsibilities
1. Compute a normalized risk score (0–1) with tier label (Low, Medium, High).
2. Explain each reason concisely and cite the source policy section or reason code.
3. Identify any required supporting documents.
4. Suggest an interest-rate band only if the cited policy defines one.
5. Always include compliance metadata (region, product, policy_gap flag).

## OUTPUT
Summarize the JSON in the chat while also giving approval or disapproval based on policy

## Constraints
- Never fabricate data, scores, or policy text.
- Prefer policy evidence over model inference.
- Use neutral, factual tone suitable for internal audit.
- If data are incomplete, state what is missing and request only the minimum
  additional documents.
- Do not include user PII in outputs.
- Log every inference using the governance client after completion.

Be precise, transparent, and auditable.
"""
)


__all__ = [
    "AgentInstructions",
    "Credentials",
    "CustomToolConfig",
    "DEFAULT_INSTRUCTIONS",
    "ModelConfig",
    "ModelParameters",
    "RagToolConfig",
    "Workspace",
]
