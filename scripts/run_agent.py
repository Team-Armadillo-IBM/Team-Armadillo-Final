"""Command line entry-point for invoking the refactored Agent Lab workflow."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Optional
from uuid import UUID

from langchain_core.messages import AIMessage, HumanMessage

from agent_lab import (
    AgentContext,
    CustomToolConfig,
    RagToolConfig,
    Workspace,
    build_agent,
    get_bearer_token,
    load_credentials,
)

POLICY_PATH = Path("docs/AutoLoanPolicy_Global_2025.md")

POLICY_TOOL_SCHEMA: dict[str, Any] = {
    "type": "object",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "additionalProperties": False,
    "properties": {
        "section": {
            "type": "string",
            "description": "Optional section title or number to retrieve (for example, 'Section 1' or 'Interest Rate Bands').",
        },
        "keyword": {
            "type": "string",
            "description": "Optional keyword to search across the policy (for example, 'DTI' or 'documentation').",
        },
    },
}

POLICY_TOOL_CODE = """
from pathlib import Path

POLICY_FILE = Path(policy_path)


def _extract_section(policy_text: str, target: str) -> str | None:
    target_lower = target.lower()
    capture: list[str] = []
    recording = False
    for line in policy_text.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("## section"):
            if recording and capture:
                break
            recording = target_lower in stripped.lower()
        if recording:
            capture.append(line)
    if capture:
        return "\n".join(capture).strip()
    return None


def _search_keyword(policy_text: str, keyword: str) -> str | None:
    keyword_lower = keyword.lower()
    matches = [line for line in policy_text.splitlines() if keyword_lower in line.lower()]
    if matches:
        return "\n".join(matches).strip()
    return None


def lookup_auto_loan_policy(section: str | None = None, keyword: str | None = None) -> str:
    policy_text = POLICY_FILE.read_text(encoding="utf-8")
    if section:
        section_text = _extract_section(policy_text, section)
        if section_text:
            return section_text
        return f"No section matching '{section}' was found in the policy."
    if keyword:
        keyword_text = _search_keyword(policy_text, keyword)
        if keyword_text:
            return keyword_text
        return f"No policy text referencing '{keyword}' was found."
    return policy_text
"""


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
    parser.add_argument(
        "question",
        nargs=argparse.REMAINDER,
        help="User question to send to the agent (no extra quoting required).",
    )
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
    args = parser.parse_args()

    if not args.question:
        parser.error("A question or prompt is required.")

    # argparse.REMAINDER returns a list of tokens; join to reconstruct the original
    # prompt so multi-word/YAML inputs can be passed without shell-escaping.
    args.question = " ".join(args.question).strip()

    return args


def _first_env_value(*names: str) -> tuple[Optional[str], Optional[str]]:
    """Return the first set environment variable from *names* and its source name."""

    for name in names:
        value = os.getenv(name)
        if value:
            return value, name
    return None, None


def _validate_guid(value: str, field: str, source: str) -> str:
    """Ensure *value* looks like a UUID before handing it to the watsonx SDK."""

    try:
        UUID(value)
    except (TypeError, ValueError) as exc:
        preview = value if len(value) <= 32 else f"{value[:8]}…{value[-6:]}"
        raise SystemExit(
            f"{field} from {source} must be a valid UUID/GUID, but the provided value "
            f"('{preview}') is not."
        ) from exc
    return value


def resolve_workspace(project_id: Optional[str], space_id: Optional[str]) -> Workspace:
    """Resolve workspace identifiers from CLI args or environment variables."""

    project_source = "--project-id"
    space_source = "--space-id"

    env_project_id, env_project_source = _first_env_value("PROJECT_ID", "WATSONX_PROJECT_ID")
    env_space_id, env_space_source = _first_env_value("SPACE_ID", "WATSONX_SPACE_ID")

    resolved_project_id = project_id or env_project_id
    project_source = project_source if project_id else env_project_source

    resolved_space_id = space_id or env_space_id
    space_source = space_source if space_id else env_space_source

    if not resolved_project_id and not resolved_space_id:
        raise SystemExit(
            "A watsonx project or space ID is required. Provide --project-id/--space-id "
            "or set PROJECT_ID/SPACE_ID (or WATSONX_PROJECT_ID/WATSONX_SPACE_ID)."
        )

    if resolved_project_id:
        resolved_project_id = _validate_guid(resolved_project_id, "project_id", project_source or "environment")
    if resolved_space_id:
        resolved_space_id = _validate_guid(resolved_space_id, "space_id", space_source or "environment")

    return Workspace(project_id=resolved_project_id, space_id=resolved_space_id)


def build_policy_tool() -> CustomToolConfig:
    if not POLICY_PATH.exists():  # pragma: no cover - guardrail for misconfigured deployments
        raise SystemExit(f"Expected policy file at {POLICY_PATH} but it was not found.")

    return CustomToolConfig(
        name="MockBankAutoLoanPolicy",
        description=(
            "Look up sections or keywords from the Mock Bank Auto Loan Policy (AutoLoanPolicy_Global_2025) "
            "to ground lending decisions."
        ),
        code=POLICY_TOOL_CODE,
        schema=POLICY_TOOL_SCHEMA,
        params={"policy_path": str(POLICY_PATH)},
    )


def main() -> None:
    args = parse_args()

    credentials, source = load_credentials()
    # Lazily fetch bearer token for external usage when requested.
    bearer_token = get_bearer_token(credentials)

    workspace = resolve_workspace(args.project_id, args.space_id)
    rag_config = RagToolConfig(vector_index_id=args.vector_index_id)
    custom_tools = [build_policy_tool()]

    agent_context = AgentContext(
        credentials=credentials,
        workspace=workspace,
        rag=rag_config,
        custom_tools=custom_tools,
    )
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
