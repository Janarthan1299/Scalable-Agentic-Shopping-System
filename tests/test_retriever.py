from app.services.tool_retriever import ToolRetriever
from app.tools.catalog import build_registry


def test_domain_filter_and_top_k():
    registry = build_registry(1000)
    results = ToolRetriever(registry).retrieve_tools("Where is my order?", "delivery", 5)
    assert len(results) == 5
    assert results[0]["tool_name"] == "track_order"
    assert all(item["metadata"].domain == "delivery" for item in results)
