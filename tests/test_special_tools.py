from app.database.database import Database
from app.tools.catalog import build_registry
from app.tools.system_search_tool import system_search


def test_rag_and_system_search():
    registry = build_registry(0)
    rag = registry.get_tool("rag_search").invoke({"query": "return policy"})
    assert "30 days" in rag["answer"]
    result = system_search("order tools", registry, Database(":memory:"))
    assert "get_order" in result["tools"]
