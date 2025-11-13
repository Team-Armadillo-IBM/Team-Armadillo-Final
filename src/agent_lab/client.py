"""Client helpers for Agent Lab."""
from __future__ import annotations

from ibm_watsonx_ai import APIClient

from .config import Credentials, Workspace


def create_api_client(credentials: Credentials, workspace: Workspace | None = None) -> APIClient:
    """Instantiate an :class:`APIClient` with the appropriate workspace identifiers."""

    workspace = workspace or Workspace()
    return APIClient(credentials={"url": credentials.url, "apikey": credentials.api_key}, **workspace.as_kwargs())


__all__ = ["create_api_client"]
