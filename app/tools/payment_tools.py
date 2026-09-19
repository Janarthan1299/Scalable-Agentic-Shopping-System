"""Local payment tools."""
from .order_tools import _find


def get_payment_status(order_id: str) -> dict[str, str]:
    _find(order_id)
    return {"order_id": order_id, "payment_status": "captured"}


def refund_payment(order_id: str) -> dict[str, str]:
    _find(order_id)
    return {"order_id": order_id, "payment_status": "refund_initiated"}
