"""Local delivery status tools."""
from .order_tools import _find


def track_order(order_id: str) -> dict[str, str]:
    order = _find(order_id)
    return {"order_id": order_id, "delivery_status": order["delivery_status"], "message": f"Order {order_id} is {order['delivery_status']}."}


def get_delivery_status(order_id: str) -> dict[str, str]:
    return track_order(order_id)
