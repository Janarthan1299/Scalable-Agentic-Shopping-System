"""Common tool metadata and execution contract."""
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class ToolMetadata:
    name: str
    description: str
    domain: str
    operation: str
    required_parameters: list[str]
    optional_parameters: list[str]
    risk_level: str = "low"
    permission: str = "public:read"
    version: str = "1.0"
    enabled: bool = True


@dataclass
class RegisteredTool:
    metadata: ToolMetadata
    handler: Callable[..., dict[str, Any]]

    def invoke(self, parameters: dict[str, Any]) -> dict[str, Any]:
        return self.handler(**parameters)
