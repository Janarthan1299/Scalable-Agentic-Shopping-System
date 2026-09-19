"""Local return tools."""
from .order_tools import _find


def create_return(order_id: str, reason: str) -> dict[str, str]:
    _find(order_id)
    return {"return_id": f"R-{order_id}", "order_id": order_id, "reason": reason, "status": "requested"}


def get_return_status(return_id: str) -> dict[str, str]:
    return {"return_id": return_id, "status": "requested"}
