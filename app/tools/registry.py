"""Central registry for real and simulated tools."""
from dataclasses import asdict
from typing import Any
from .base import RegisteredTool, ToolMetadata


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, RegisteredTool] = {}

    def register_tool(self, tool: RegisteredTool) -> None:
        self._tools[tool.metadata.name] = tool

    def get_tool(self, name: str) -> RegisteredTool:
        if name not in self._tools:
            raise KeyError(f"Tool not found: {name}")
        return self._tools[name]

    def list_tools(self, enabled_only: bool = True) -> list[RegisteredTool]:
        values = self._tools.values()
        return [tool for tool in values if tool.metadata.enabled or not enabled_only]

    def get_tool_metadata(self, name: str) -> dict[str, Any]:
        return asdict(self.get_tool(name).metadata)

    def get_tools_by_domain(self, domain: str) -> list[RegisteredTool]:
        return [tool for tool in self.list_tools() if tool.metadata.domain == domain]

    def search_tools(self, query: str, domain: str | None = None) -> list[RegisteredTool]:
        terms = set(query.lower().split())
        tools = self.get_tools_by_domain(domain) if domain else self.list_tools()
        scored = []
        for tool in tools:
            text = f"{tool.metadata.name} {tool.metadata.description} {tool.metadata.operation}".lower()
            score = sum(1 for term in terms if term in text)
            if score:
                scored.append((score, tool))
        return [tool for _, tool in sorted(scored, key=lambda item: (-item[0], item[1].metadata.name))]

    def __len__(self) -> int:
        return len(self._tools)


def generate_mock_tools(registry: ToolRegistry, count: int = 1000) -> None:
    """Register inert tools to demonstrate registry scale without exposing them."""
    domains = ["product", "order", "customer", "delivery", "payment", "return", "knowledge", "system"]
    for index in range(1, count + 1):
        name = f"product_tool_{index:03d}"
        metadata = ToolMetadata(name, f"Simulated capability {index}", domains[index % len(domains)], "simulate", [], [])
        registry.register_tool(RegisteredTool(metadata, lambda tool_name=name, **_: {"simulated": True, "tool": tool_name}))
