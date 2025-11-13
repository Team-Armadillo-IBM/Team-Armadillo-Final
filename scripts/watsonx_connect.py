"""Legacy wrapper retained for backwards compatibility."""
from __future__ import annotations

from agent_lab import get_bearer_token, load_credentials


def get_iam_token(api_key: str | None = None) -> str:
    """Generate an IBM Cloud IAM token using the provided API key."""

    credentials, _ = load_credentials(api_key=api_key, prompt=api_key is None)
    token = get_bearer_token(credentials)
    print("✅ IBM Cloud IAM token generated.")
    return token


__all__ = ["get_iam_token"]
