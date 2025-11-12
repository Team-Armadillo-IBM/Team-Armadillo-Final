"""Command line entry-point for invoking the refactored Agent Lab workflow."""
from __future__ import annotations

import argparse
import json
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage

from agent_lab import (
    AgentContext,
    RagToolConfig,
    Workspace,
    build_agent,
    get_bearer_token,
    load_credentials,
)


def convert_messages(messages: list[dict[str, Any]]):
    converted_messages = []
    for message in messages:
        if message["role"] == "user":
            converted_messages.append(HumanMessage(content=message["content"]))
        elif message["role"] == "assistant":
            converted_messages.append(AIMessage(content=message["content"]))
    return converted_messages


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Invoke the Loan Risk Assistant agent.")
    parser.add_argument("question", help="User question to send to the agent.")
    parser.add_argument(
        "--vector-index-id",
        default="40824957-150a-4607-a08c-7f8885b0befa",
        help="Vector index identifier used by the RAG tool.",
    )
    parser.add_argument(
        "--project-id",
        default=None,
        help="Optional watsonx project identifier.",
    )
    parser.add_argument(
        "--space-id",
        default=None,
        help="Optional watsonx space identifier.",
    )
    parser.add_argument(
        "--print-full-response",
        action="store_true",
        help="Print the raw agent response payload for debugging.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    credentials, source = load_credentials()
    # Lazily fetch bearer token for external usage when requested.
    bearer_token = get_bearer_token(credentials)

    workspace = Workspace(project_id=args.project_id, space_id=args.space_id)
    rag_config = RagToolConfig(vector_index_id=args.vector_index_id)

    agent_context = AgentContext(credentials=credentials, workspace=workspace, rag=rag_config)
    agent = build_agent(agent_context)

    messages = [{"role": "user", "content": args.question}]
    response = agent.invoke({"messages": convert_messages(messages)}, {"configurable": {"thread_id": "42"}})

    if args.print_full_response:
        print(json.dumps(response, indent=2))
    else:
        print(response["messages"][-1].content)

    # Print credential provenance to aid debugging when run interactively.
    print("\nCredential source:")
    print(json.dumps(source.__dict__, indent=2))
    print("Bearer token acquired:", bool(bearer_token))


if __name__ == "__main__":
    main()
