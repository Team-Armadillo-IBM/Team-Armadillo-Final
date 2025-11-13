"""Authentication helpers for watsonx.ai."""
from __future__ import annotations

import os
from dataclasses import dataclass
from getpass import getpass
from typing import Optional

import requests

from .config import Credentials


class AuthenticationError(RuntimeError):
    """Raised when IAM authentication fails."""


@dataclass
class CredentialSource:
    """Describe where credentials were loaded from for traceability."""

    api_key_env: Optional[str] = None
    url_env: Optional[str] = None
    prompted: bool = False


def load_credentials(
    *,
    api_key: Optional[str] = None,
    url: Optional[str] = None,
    prompt: bool = True,
) -> tuple[Credentials, CredentialSource]:
    """Load credentials from parameters, environment variables, or interactive prompt."""

    source = CredentialSource()

    resolved_api_key = api_key or os.getenv("IBM_API_KEY")
    if resolved_api_key:
        source.api_key_env = "IBM_API_KEY" if api_key is None else None
    elif prompt:
        resolved_api_key = getpass("Please enter your api key (hit enter): ")
        source.prompted = True

    if not resolved_api_key:
        raise AuthenticationError("An IBM Cloud API key is required to authenticate.")

    resolved_url = url or os.getenv("WATSONX_URL") or "https://us-south.ml.cloud.ibm.com"
    if url is None and os.getenv("WATSONX_URL"):
        source.url_env = "WATSONX_URL"

    return Credentials(url=resolved_url, api_key=resolved_api_key), source


def get_bearer_token(credentials: Credentials) -> str:
    """Request an IAM access token for the provided credentials."""

    token_url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": credentials.api_key,
    }
    response = requests.post(token_url, headers=headers, data=data, timeout=30)
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:  # pragma: no cover - just defensive logging
        raise AuthenticationError(f"Failed to obtain IAM token: {exc}") from exc

    token = response.json().get("access_token")
    if not token:
        raise AuthenticationError("IAM token response did not include an access_token field.")

    return token


__all__ = ["AuthenticationError", "CredentialSource", "Credentials", "get_bearer_token", "load_credentials"]
