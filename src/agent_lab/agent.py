"""Agent creation utilities."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from ibm_watsonx_ai.deployments import RuntimeContext
from langchain_ibm import ChatWatsonx
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from .client import create_api_client
from .config import (
    AgentInstructions,
    Credentials,
    CustomToolConfig,
    DEFAULT_INSTRUCTIONS,
    ModelConfig,
    RagToolConfig,
    Workspace,
)
from .tools import assemble_toolkit


@dataclass
class AgentContext:
    """Container bundling all dependencies required to build the agent."""

    credentials: Credentials
    workspace: Workspace = Workspace()
    model: ModelConfig = ModelConfig()
    instructions: AgentInstructions = DEFAULT_INSTRUCTIONS
    rag: Optional[RagToolConfig] = None
    custom_tools: Iterable[CustomToolConfig] = ()
    include_python_tool: bool = True
    include_google_search: bool = True


def create_chat_model(agent_context: AgentContext, api_client) -> ChatWatsonx:
    """Instantiate the chat model using the context configuration."""

    return ChatWatsonx(
        model_id=agent_context.model.model_id,
        url=agent_context.credentials.url,
        space_id=agent_context.workspace.space_id,
        project_id=agent_context.workspace.project_id,
        params=agent_context.model.parameters.as_dict(),
        watsonx_client=api_client,
    )


def build_agent(agent_context: AgentContext):
    """Create the LangGraph ReAct agent using the supplied configuration."""

    api_client = create_api_client(agent_context.credentials, agent_context.workspace)
    chat_model = create_chat_model(agent_context, api_client)
    runtime_context = RuntimeContext(api_client=api_client)

    tools = assemble_toolkit(
        api_client=api_client,
        context=runtime_context,
        workspace=agent_context.workspace,
        rag_config=agent_context.rag,
        include_python=agent_context.include_python_tool,
        include_google_search=agent_context.include_google_search,
        custom_tools=agent_context.custom_tools,
    )

    memory = MemorySaver()

    agent = create_react_agent(
        chat_model,
        tools=tools,
        checkpointer=memory,
        prompt=agent_context.instructions.instructions,
    )
    return agent


__all__ = ["AgentContext", "build_agent", "create_chat_model"]
