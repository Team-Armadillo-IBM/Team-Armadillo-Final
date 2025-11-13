"""High-level API for constructing Agent Lab agents."""
from .agent import AgentContext, build_agent, create_chat_model
from .auth import AuthenticationError, CredentialSource, get_bearer_token, load_credentials
from .client import create_api_client
from .config import (
    AgentInstructions,
    Credentials,
    CustomToolConfig,
    DEFAULT_INSTRUCTIONS,
    ModelConfig,
    ModelParameters,
    RagToolConfig,
    Workspace,
)
from .tools import assemble_toolkit

__all__ = [
    "AgentContext",
    "AgentInstructions",
    "AuthenticationError",
    "CredentialSource",
    "Credentials",
    "CustomToolConfig",
    "DEFAULT_INSTRUCTIONS",
    "ModelConfig",
    "ModelParameters",
    "RagToolConfig",
    "Workspace",
    "assemble_toolkit",
    "build_agent",
    "create_api_client",
    "create_chat_model",
    "get_bearer_token",
    "load_credentials",
]
