"""Tooling utilities extracted from the Agent Lab notebook."""
from __future__ import annotations

import ast
import base64
import os
import sys
import uuid
from dataclasses import dataclass
from io import StringIO
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional

import requests
from ibm_watsonx_ai.deployments import RuntimeContext
from ibm_watsonx_ai.foundation_models.utils import Toolkit
from langchain_core.tools import StructuredTool

from .config import CustomToolConfig, RagToolConfig, Workspace


@dataclass
class PythonExecutionResult:
    """Container for results returned by the Python interpreter tool."""

    output: str
    image_url: Optional[str] = None

    def as_text(self) -> str:
        if self.image_url:
            return f"Result of executing generated Python code is an image:\n\nIMAGE({self.image_url})"
        return self.output


def _get_image_url(base_64_content: str, image_name: str, context: RuntimeContext, project_id: Optional[str]) -> str:
    url = "https://api.dataplatform.cloud.ibm.com"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {context.get_token()}"
    }

    body = {
        "name": image_name,
        "blob": base_64_content
    }

    params: MutableMapping[str, Any] = {}
    if project_id:
        params["project_id"] = project_id

    response = requests.post(
        f"{url}/wx/v1-beta/utility_agent_tools/resources",
        headers=headers,
        json=body,
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    return response.json().get("uri", "")


def create_python_interpreter_tool(context: RuntimeContext, workspace: Workspace | None = None) -> StructuredTool:
    """Expose a safe Python execution environment as a LangChain tool."""

    workspace = workspace or Workspace()
    project_id = workspace.project_id
    original_import = __import__

    def pyplot_show():
        picture_name = f"plt-{uuid.uuid4().hex}.png"
        plt = sys.modules["matplotlib.pyplot"]
        plt.savefig(picture_name)
        with open(picture_name, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            os.remove(picture_name)
        plt.clf()
        plt.close("all")
        # Mirror the notebook behaviour by printing a base64 sentinel captured by stdout.
        print(f"base64image:{picture_name}:{encoded_string}")

    def patched_import(name, globals=None, locals=None, fromlist=(), level=0):  # type: ignore[override]
        module = original_import(name, globals, locals, fromlist, level)
        if name == "matplotlib.pyplot":
            sys.modules["matplotlib.pyplot"].show = lambda: pyplot_show()
        return module

    def init_imports():
        import builtins

        builtins.__import__ = patched_import

    def _execute_agent_code(code: str) -> str:
        old_stdout = sys.stdout
        redirected_output = StringIO("")
        result: PythonExecutionResult | None = None
        try:
            full_code = "init_imports()\n\n" + code
            tree = ast.parse(full_code, mode="exec")
            compiled_code = compile(tree, "agent_code", "exec")
            namespace = {"init_imports": init_imports, "PythonExecutionResult": PythonExecutionResult}
            sys.stdout = redirected_output
            exec(compiled_code, namespace)
        except Exception as exc:  # pragma: no cover - safety net
            return f"Error while executing Python code:\n\n{exc}"
        finally:
            sys.stdout = old_stdout

        value = redirected_output.getvalue()
        if value.startswith("base64image"):
            _, image_name, base_64_image = value.split(":", 2)
            image_url = _get_image_url(base_64_image, image_name, context, project_id)
            result = PythonExecutionResult(output="", image_url=image_url)
        elif isinstance(namespace.get("_"), PythonExecutionResult):
            result = namespace["_"]

        if result:
            return result.as_text()
        return value

    tool_schema: Mapping[str, Any] = {
        "type": "object",
        "$schema": "http://json-schema.org/draft-07/schema#",
        "properties": {
            "code": {
                "description": "Code to be executed.",
                "type": "string",
            }
        },
        "required": ["code"],
    }

    description = (
        "Run Python code and return the console output. Use for isolated calculations, computations or data manipulation. "
        "In Python, the following modules are available: Use numpy, pandas, scipy and sympy for working with data. Use matplotlib"
        " to plot charts. Other Python libraries are also available -- however, prefer using the ones above. Prefer using "
        "qualified imports -- `import library; library.thing()` instead of `import thing from library`. Do not attempt to install"
        " libraries manually -- it will not work. Do not use this tool multiple times in a row, always write the full code you "
        "want to run in a single invocation. If you get an error running Python code, try to generate a better one that will pass."
        " If the tool returns result that starts with IMAGE(, follow instructions for rendering images."
    )

    return StructuredTool(
        name="PythonInterpreter",
        description=description,
        func=_execute_agent_code,
        args_schema=tool_schema,
    )


def create_utility_agent_tool(
    tool_name: str,
    params: Optional[Mapping[str, Any]],
    api_client,
    *,
    override_description: Optional[str] = None,
) -> StructuredTool:
    """Instantiate a watsonx utility agent tool with LangChain bindings."""

    utility_agent_tool = Toolkit(api_client=api_client).get_tool(tool_name)

    description = override_description or utility_agent_tool.get("agent_description") or utility_agent_tool.get("description")

    tool_schema = utility_agent_tool.get("input_schema") or {
        "type": "object",
        "additionalProperties": False,
        "$schema": "http://json-schema.org/draft-07/schema#",
        "properties": {
            "input": {
                "description": "input for the tool",
                "type": "string",
            }
        },
    }

    def run_tool(**tool_input: Any) -> Any:
        query: Any = tool_input
        if utility_agent_tool.get("input_schema") is None:
            query = tool_input.get("input")

        results = utility_agent_tool.run(input=query, config=params)
        return results.get("output")

    return StructuredTool(name=tool_name, description=description, func=run_tool, args_schema=tool_schema)


def _workspace_rag_params(workspace: Workspace | None = None) -> dict[str, str]:
    params: dict[str, str] = {}
    if not workspace:
        return params

    if workspace.project_id:
        params["projectId"] = workspace.project_id
    if workspace.space_id:
        params["spaceId"] = workspace.space_id
    return params


def create_rag_tool(
    config: RagToolConfig,
    api_client,
    workspace: Workspace | None = None,
) -> StructuredTool:
    params = {"vectorIndexId": config.vector_index_id, **_workspace_rag_params(workspace)}
    return create_utility_agent_tool(
        "RAGQuery",
        params,
        api_client,
        override_description=config.description,
    )


def compile_custom_tool(tool_config: CustomToolConfig) -> StructuredTool:
    """Compile a Python function definition into a LangChain tool."""

    def call_tool(**kwargs: Any) -> Any:
        tree = ast.parse(tool_config.code, mode="exec")
        custom_tool_functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        if not custom_tool_functions:
            raise ValueError("Custom tool code must define at least one function.")
        function_name = custom_tool_functions[0].name
        compiled_code = compile(tree, "custom_tool", "exec")
        namespace: dict[str, Any] = {}
        if tool_config.params:
            namespace.update(tool_config.params)
        exec(compiled_code, namespace)
        return namespace[function_name](**kwargs)

    return StructuredTool(
        name=tool_config.name,
        description=tool_config.description,
        func=call_tool,
        args_schema=tool_config.schema,
    )


def assemble_toolkit(
    *,
    api_client,
    context: RuntimeContext,
    workspace: Workspace | None = None,
    rag_config: RagToolConfig | None = None,
    include_python: bool = True,
    include_google_search: bool = True,
    custom_tools: Iterable[CustomToolConfig] | None = None,
) -> List[StructuredTool]:
    """Construct the tool list for the agent."""

    tools: List[StructuredTool] = []

    if rag_config:
        tools.append(create_rag_tool(rag_config, api_client, workspace))

    if include_python:
        tools.append(create_python_interpreter_tool(context, workspace))

    if include_google_search:
        tools.append(create_utility_agent_tool("GoogleSearch", None, api_client))

    for tool_config in custom_tools or []:
        tools.append(compile_custom_tool(tool_config))

    return tools


__all__ = [
    "assemble_toolkit",
    "compile_custom_tool",
    "create_python_interpreter_tool",
    "create_rag_tool",
    "create_utility_agent_tool",
]
