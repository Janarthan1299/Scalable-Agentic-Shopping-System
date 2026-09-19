from app.tools.catalog import build_registry


def test_registry_has_real_tools_and_scale():
    registry = build_registry(1000)
    assert len(registry) == 1018
    assert registry.get_tool("track_order").metadata.domain == "delivery"


def test_product_tool_works():
    result = build_registry(0).get_tool("search_products").invoke({"query": "laptop", "max_price": 50000})
    assert result["count"] == 3
