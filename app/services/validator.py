"""Pydantic validation before gateway execution."""
from typing import Any, Type
from pydantic import BaseModel, ValidationError
from app.models.schemas import (
    SearchProductRequest, ProductRequest, ProductCompareRequest, OrderRequest,
    CreateOrderRequest, UpdateOrderRequest, CustomerRequest, UpdateCustomerRequest,
    ReturnRequest, ReturnStatusRequest, QueryRequest,
)

SCHEMAS: dict[str, Type[BaseModel]] = {
    "search_products": SearchProductRequest, "get_product_details": ProductRequest,
    "check_product_stock": ProductRequest, "compare_products": ProductCompareRequest,
    "get_order": OrderRequest, "cancel_order": OrderRequest, "update_order": UpdateOrderRequest,
    "create_order": CreateOrderRequest, "get_customer": CustomerRequest,
    "update_customer": UpdateCustomerRequest, "track_order": OrderRequest,
    "get_delivery_status": OrderRequest, "get_payment_status": OrderRequest,
    "refund_payment": OrderRequest, "create_return": ReturnRequest,
    "get_return_status": ReturnStatusRequest, "rag_search": QueryRequest,
    "system_search": QueryRequest,
}


class ParameterValidator:
    def validate(self, tool_name: str, parameters: dict[str, Any]) -> dict[str, Any]:
        schema = SCHEMAS.get(tool_name)
        if schema is None:
            return parameters
        try:
            return schema.model_validate(parameters).model_dump()
        except ValidationError as exc:
            raise ValueError(f"Invalid parameters for {tool_name}: {exc.errors()}") from exc
