"""Local customer tools."""
import json
from pathlib import Path
from typing import Any


def _customers() -> list[dict[str, Any]]:
    return json.loads((Path(__file__).parents[2] / "data" / "customers.json").read_text())


def get_customer(customer_id: str) -> dict[str, Any]:
    customer = next((c for c in _customers() if c["customer_id"] == customer_id), None)
    if not customer:
        raise ValueError(f"Customer {customer_id} was not found")
    return customer


def update_customer(customer_id: str, update_data: dict[str, Any]) -> dict[str, Any]:
    customer = get_customer(customer_id)
    customer.update(update_data)
    return customer
