"""LangGraph workflow with a deterministic fallback runner."""
import json
import logging
import uuid
from typing import Any
from app.agent.executor import ToolGateway
from app.agent.planner import Planner
from app.agent.router import RequestRouter
from app.models.state import AgentState
from app.services.tool_retriever import ToolRetriever

logger = logging.getLogger(__name__)


class ShoppingAgent:
    def __init__(self, registry, gateway: ToolGateway, retriever: ToolRetriever, top_k: int = 5) -> None:
        self.registry, self.gateway, self.retriever, self.top_k = registry, gateway, retriever, top_k
        self.router, self.planner = RequestRouter(), Planner()
        self.graph = self._build_graph()

    def _build_graph(self):
        try:
            from langgraph.graph import StateGraph, START, END
            workflow = StateGraph(AgentState)
            workflow.add_node("analyze_request", self.analyze_request)
            workflow.add_node("route_request", self.route_request)
            workflow.add_node("retrieve_tools", self.retrieve_tools)
            workflow.add_node("plan_task", self.plan_task)
            workflow.add_node("execute_tool", self.execute_tool)
            workflow.add_node("validate_result", self.validate_result)
            workflow.add_node("retry_or_replan", self.retry_or_replan)
            workflow.add_node("generate_response", self.generate_response)
            workflow.add_edge(START, "analyze_request"); workflow.add_edge("analyze_request", "route_request"); workflow.add_edge("route_request", "retrieve_tools"); workflow.add_edge("retrieve_tools", "plan_task"); workflow.add_edge("plan_task", "execute_tool"); workflow.add_edge("execute_tool", "validate_result")
            workflow.add_conditional_edges("validate_result", lambda state: "retry_or_replan" if state.get("errors") else ("execute_tool" if state["current_step"] < len(state["plan"]) else "generate_response"), {"retry_or_replan": "retry_or_replan", "execute_tool": "execute_tool", "generate_response": "generate_response"})
            workflow.add_edge("retry_or_replan", "generate_response"); workflow.add_edge("generate_response", END)
            return workflow.compile()
        except ImportError:
            return None

    def analyze_request(self, state: AgentState) -> AgentState:
        state["request_id"] = state.get("request_id", f"REQ-{uuid.uuid4().hex[:8].upper()}")
        state.setdefault("current_step", 0); state.setdefault("retry_count", 0); state.setdefault("errors", []); state.setdefault("tool_results", []); state.setdefault("completed_steps", [])
        return state

    def route_request(self, state: AgentState) -> AgentState:
        state["domain"], state["intent"] = self.router.route(state["user_query"])
        return state

    def retrieve_tools(self, state: AgentState) -> AgentState:
        state["candidate_tools"] = self.retriever.retrieve_tools(state["user_query"], state["domain"], self.top_k)
        state["selected_tools"] = [item["tool_name"] for item in state["candidate_tools"]]
        logger.info("request_id=%s total_tools=%s retrieved_tools=%s selected=%s", state["request_id"], len(self.registry), len(state["selected_tools"]), state["selected_tools"])
        return state

    def plan_task(self, state: AgentState) -> AgentState:
        state["plan"] = self.planner.plan(state["user_query"], state["domain"], state["intent"])
        state["current_step"] = 0
        return state

    def execute_tool(self, state: AgentState) -> AgentState:
        step = state["plan"][state["current_step"]]
        state["current_tool"] = step["tool"]
        try:
            result = self.gateway.execute(state["request_id"], state["user_id"], step["tool"], step["parameters"])
            state["tool_results"].append({"tool": step["tool"], "result": result})
        except Exception as exc:
            state["errors"].append(str(exc))
        return state

    def validate_result(self, state: AgentState) -> AgentState:
        if state.get("errors"):
            return state
        state["completed_steps"].append(state["current_tool"] or "")
        state["current_step"] += 1
        return state

    def retry_or_replan(self, state: AgentState) -> AgentState:
        state["retry_count"] += 1
        return state

    def generate_response(self, state: AgentState) -> AgentState:
        if state.get("errors"):
            state["status"] = "error"; state["final_response"] = f"I could not complete the request: {state['errors'][-1]}"
        else:
            results = state.get("tool_results", [])
            last = results[-1]["result"] if results else {}
            if state["intent"] == "system_search": state["final_response"] = "Available order tools: " + ", ".join(last.get("tools", []))
            elif state["intent"] == "return_policy" or state["domain"] == "knowledge": state["final_response"] = last.get("answer", "No knowledge-base answer found.")
            elif state["domain"] == "delivery": state["final_response"] = last.get("message", str(last))
            elif state["intent"] == "check_product_stock": state["final_response"] = f"Product {last.get('product_id')} is {'in stock' if last.get('in_stock') else 'out of stock'} ({last.get('stock', 0)} available)."
            else: state["final_response"] = "Completed: " + json.dumps(last, default=str)
            state["status"] = "success"
        return state

    def invoke(self, user_id: str, query: str) -> AgentState:
        state: AgentState = {"user_id": user_id, "user_query": query}
        if self.graph:
            return self.graph.invoke(state)
        for node in (self.analyze_request, self.route_request, self.retrieve_tools, self.plan_task): state = node(state)
        while state["current_step"] < len(state["plan"]):
            state = self.execute_tool(state); state = self.validate_result(state)
            if state.get("errors"): break
        return self.generate_response(state)
