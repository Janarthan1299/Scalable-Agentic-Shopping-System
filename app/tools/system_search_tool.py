"""Search registry capabilities and persisted request history."""
from typing import Any
from app.database.database import Database
from app.tools.registry import ToolRegistry


def system_search(query: str, registry: ToolRegistry, database: Database) -> dict[str, Any]:
    lowered = query.lower()
    tools = registry.search_tools(query)
    if "order" in lowered:
        tools = [tool for tool in registry.list_tools() if tool.metadata.domain in {"order", "delivery"}]
    history = database.search_history(query)
    return {"tools": [tool.metadata.name for tool in tools[:10]], "requests": history}
