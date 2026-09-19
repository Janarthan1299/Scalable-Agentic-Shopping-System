"""FastAPI application and dependency wiring."""
import logging
import sys
from pathlib import Path

# Ensure project root is in sys.path when running script directly from subdirectories
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from app.agent.executor import ToolGateway
from app.agent.graph import ShoppingAgent
from app.config import get_settings
from app.database.database import Database
from app.database.seed import seed_database
from app.models.schemas import ChatRequest, ChatResponse
from app.services.audit_service import AuditService
from app.services.tool_retriever import ToolRetriever
from app.tools.catalog import build_registry
from app.tools.system_search_tool import system_search
from app.utils.logger import configure_logging

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger(__name__)


def create_agent() -> ShoppingAgent:
    registry = build_registry(1000)
    database = Database()
    seed_database(database, registry)
    registry.get_tool("system_search").handler = lambda query: system_search(query, registry, database)
    audit = AuditService(database)
    gateway = ToolGateway(registry, audit, max_retries=settings.max_retries)
    return ShoppingAgent(registry, gateway, ToolRetriever(registry), settings.top_k)


agent = create_agent()
app = FastAPI(title=settings.app_name, version="1.0.0")

# Path to static frontend
static_dir = Path(__file__).resolve().parent / "static"


@app.get("/", response_class=HTMLResponse)
def root() -> HTMLResponse:
    index_file = static_dir / "index.html"
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Scalable Agentic Shopping System</h1><p>API documentation is available at <a href='/docs'>/docs</a>.</p>")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    state = agent.invoke(request.user_id, request.message)
    return ChatResponse(request_id=state["request_id"], response=state["final_response"], tools_used=state.get("completed_steps", []), status=state.get("status", "error"))


@app.get("/tools")
def tools() -> list[dict]:
    return [tool.metadata.__dict__ for tool in agent.registry.list_tools()]


@app.get("/tools/{tool_name}")
def tool(tool_name: str) -> dict:
    try: return agent.registry.get_tool_metadata(tool_name)
    except KeyError as exc: raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/requests/{request_id}")
def request_history(request_id: str) -> dict:
    result = agent.gateway.audit.database.get_request(request_id)
    if not result: raise HTTPException(status_code=404, detail="Request not found")
    return result


@app.get("/system/search")
def system_search_endpoint(query: str = Query(min_length=1)) -> dict:
    return system_search(query, agent.registry, agent.gateway.audit.database)


@app.get("/rag/search")
def rag_search_endpoint(query: str = Query(min_length=1)) -> dict:
    return agent.registry.get_tool("rag_search").invoke({"query": query})


@app.get("/demo/scalability")
def scalability_demo() -> dict:
    state = agent.invoke("C001", "Where is my order O10025?")
    return {"total_registered_tools": len(agent.registry), "query": state["user_query"], "domain": state["domain"], "candidate_tools": state["candidate_tools"], "tools_exposed_to_agent": len(state["selected_tools"]), "selected_tools": state["selected_tools"], "response": state["final_response"]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
