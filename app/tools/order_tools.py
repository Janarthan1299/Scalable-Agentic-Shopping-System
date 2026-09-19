"""Local order tools."""
import json
from pathlib import Path
from typing import Any


def _orders() -> list[dict[str, Any]]:
    return json.loads((Path(__file__).parents[2] / "data" / "orders.json").read_text())


def _find(order_id: str) -> dict[str, Any]:
    order = next((o for o in _orders() if o["order_id"] == order_id), None)
    if not order:
        raise ValueError(f"Order {order_id} was not found")
    return order


def create_order(customer_id: str, product_id: str, quantity: int) -> dict[str, Any]:
    return {"order_id": "O" + str(2000 + len(_orders())), "customer_id": customer_id, "product_id": product_id, "quantity": quantity, "status": "created"}


def get_order(order_id: str) -> dict[str, Any]:
    return _find(order_id)


def cancel_order(order_id: str) -> dict[str, Any]:
    order = _find(order_id)
    if order["status"] == "cancelled":
        return order
    order["status"] = "cancelled"
    return order


def update_order(order_id: str, update_data: dict[str, Any]) -> dict[str, Any]:
    order = _find(order_id)
    order.update(update_data)
    return order
