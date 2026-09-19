"""Deterministic planner; an LLM planner can replace this boundary later."""
import re
from typing import Any


class Planner:
    def plan(self, query: str, domain: str, intent: str) -> list[dict[str, Any]]:
        text = query.lower()
        order_id_match = re.search(r"\bO\d+\b", query, re.I)
        order_id = order_id_match.group(0).upper() if order_id_match else "O10025"
        product_id_match = re.search(r"\bP\d+\b", query, re.I)
        product_id = product_id_match.group(0).upper() if product_id_match else None
        price_match = re.search(r"(?:under|below)\s*(\d+)", text)
        max_price = float(price_match.group(1)) if price_match else None
        if domain == "system": return [{"tool": "system_search", "parameters": {"query": query}}]
        if domain == "knowledge": return [{"tool": "rag_search", "parameters": {"query": query}}]
        if "cancel" in text: return [{"tool": "get_order", "parameters": {"order_id": order_id}}, {"tool": "cancel_order", "parameters": {"order_id": order_id}}]
        if domain == "delivery": return [{"tool": "track_order", "parameters": {"order_id": order_id}}]
        if intent == "check_product_stock": return [{"tool": "check_product_stock", "parameters": {"product_id": product_id or "P001"}}]
        if domain == "product":
            steps = [{"tool": "search_products", "parameters": {"query": "laptop", **({"max_price": max_price} if max_price else {})}}]
            if "highest" in text or "rating" in text:
                steps.extend([{"tool": "compare_products", "parameters": {"product_ids": ["P001", "P003", "P004"]}}, {"tool": "check_product_stock", "parameters": {"product_id": "P001"}}])
            return steps
        return [{"tool": "rag_search", "parameters": {"query": query}}]
