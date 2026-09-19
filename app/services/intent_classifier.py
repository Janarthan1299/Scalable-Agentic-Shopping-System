"""Deterministic intent classifier with an LLM-compatible boundary."""
from dataclasses import dataclass


@dataclass
class Intent:
    domain: str
    intent: str


class IntentClassifier:
    def classify(self, query: str) -> Intent:
        text = query.lower()
        if any(word in text for word in ("tool", "capabilit", "previous request", "last request", "history")):
            return Intent("system", "system_search")
        if any(word in text for word in ("return policy", "shipping policy", "warranty", "faq", "can i return")):
            return Intent("knowledge", "return_policy" if "return" in text else "knowledge_search")
        if any(word in text for word in ("cancel", "create order", "update order")):
            return Intent("order", "cancel_order" if "cancel" in text else "order_action")
        if any(word in text for word in ("stock", "in stock", "available")) and "product" in text:
            return Intent("product", "check_product_stock")
        if any(word in text for word in ("order", "delivered", "delivery", "track")):
            return Intent("delivery", "track_order")
        if any(word in text for word in ("laptop", "product", "find", "under", "below", "price")):
            return Intent("product", "search_product")
        return Intent("knowledge", "knowledge_search")
