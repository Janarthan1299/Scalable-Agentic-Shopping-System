from app.agent.executor import ToolGateway
from app.agent.graph import ShoppingAgent
from app.database.database import Database
from app.services.audit_service import AuditService
from app.services.tool_retriever import ToolRetriever
from app.tools.catalog import build_registry


def make_agent():
    registry = build_registry(1000)
    database = Database(":memory:")
    return ShoppingAgent(registry, ToolGateway(registry, AuditService(database)), ToolRetriever(registry), 5)


def test_delivery_workflow():
    state = make_agent().invoke("C001", "Where is my order O10025?")
    assert state["status"] == "success"
    assert state["completed_steps"] == ["track_order"]
    assert "out for delivery" in state["final_response"]


def test_multi_step_workflow():
    state = make_agent().invoke("C001", "Cancel order O10025")
    assert state["completed_steps"] == ["get_order", "cancel_order"]


def test_knowledge_workflow():
    state = make_agent().invoke("C001", "What is the shipping policy?")
    assert "shipping" in state["final_response"].lower()
