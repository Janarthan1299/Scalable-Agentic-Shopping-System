"""Local product catalog tools."""
import json
from pathlib import Path
from typing import Any


def _products() -> list[dict[str, Any]]:
    return json.loads((Path(__file__).parents[2] / "data" / "products.json").read_text())


def search_products(query: str, max_price: float | None = None) -> dict[str, Any]:
    terms = query.lower().split()
    matches = [p for p in _products() if any(term in p["name"].lower() or term in p["category"] for term in terms)]
    if not matches:
        matches = [p for p in _products() if p["category"] in query.lower()]
    if max_price is not None:
        matches = [p for p in matches if p["price"] <= max_price]
    return {"products": matches, "count": len(matches)}


def get_product_details(product_id: str) -> dict[str, Any]:
    product = next((p for p in _products() if p["product_id"] == product_id), None)
    if not product:
        raise ValueError(f"Product {product_id} was not found")
    return product


def check_product_stock(product_id: str) -> dict[str, Any]:
    product = get_product_details(product_id)
    return {"product_id": product_id, "in_stock": product["stock"] > 0, "stock": product["stock"]}


def compare_products(product_ids: list[str]) -> dict[str, Any]:
    products = [get_product_details(product_id) for product_id in product_ids]
    return {"products": sorted(products, key=lambda item: item["rating"], reverse=True), "highest_rated": max(products, key=lambda item: item["rating"])}
