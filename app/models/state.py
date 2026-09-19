"""State carried through the agent graph."""
from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    request_id: str
    user_id: str
    user_query: str
    domain: str
    intent: str
    candidate_tools: list[dict[str, Any]]
    selected_tools: list[str]
    current_tool: str | None
    current_step: int
    plan: list[dict[str, Any]]
    completed_steps: list[str]
    tool_results: list[dict[str, Any]]
    errors: list[str]
    retry_count: int
    final_response: str
    status: str
