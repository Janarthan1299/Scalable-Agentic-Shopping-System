"""Top-K retrieval over registry metadata."""
import re
from typing import Any
from app.tools.registry import ToolRegistry


class ToolRetriever:
    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    def retrieve_tools(self, query: str, domain: str | None, top_k: int = 5) -> list[dict[str, Any]]:
        terms = set(re.findall(r"[a-z0-9]+", query.lower()))
        candidates = self.registry.get_tools_by_domain(domain) if domain else self.registry.list_tools()
        scored = []
        for tool in candidates:
            metadata = tool.metadata
            searchable = set(re.findall(r"[a-z0-9]+", f"{metadata.name} {metadata.description} {metadata.operation}".lower()))
            score = len(terms.intersection(searchable)) / max(len(terms), 1)
            if metadata.name in {"track_order", "search_products", "rag_search", "system_search"}:
                score += 0.2
            scored.append({"tool_name": metadata.name, "score": round(score, 3), "metadata": metadata})
        return sorted(scored, key=lambda item: (-item["score"], item["tool_name"]))[:top_k]
