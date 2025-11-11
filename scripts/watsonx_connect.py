"""Helper functions for authenticating with IBM Cloud and calling the Granite API."""

from __future__ import annotations

import json
import os
from typing import Any, Dict

import requests


def get_iam_token(api_key: str) -> str:
    """Retrieve an IAM access token for the provided IBM Cloud API key."""
    url = "https://iam.cloud.ibm.com/identity/token"
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=data, headers=headers, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return payload["access_token"]


def invoke_granite_model(*, api_key: str, project_id: str, endpoint: str, prompt: str, **params: Any) -> Dict[str, Any]:
    """Call a Granite model deployment with a text prompt and return the JSON response."""
    token = get_iam_token(api_key)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    body = {
        "input": prompt,
        "project_id": project_id,
        **params,
    }
    response = requests.post(endpoint, headers=headers, data=json.dumps(body), timeout=60)
    response.raise_for_status()
    return response.json()


def resolve_env_variable(name: str) -> str:
    """Read a required environment variable, raising an informative error if missing."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Environment variable '{name}' is required for watsonx connectivity.")
    return value


__all__ = ["get_iam_token", "invoke_granite_model", "resolve_env_variable"]
