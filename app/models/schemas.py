"""API and tool parameter schemas."""
from typing import Any
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_id: str = "C001"
    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    request_id: str
    response: str
    tools_used: list[str]
    status: str


class SearchProductRequest(BaseModel):
    query: str = Field(min_length=1)
    max_price: float | None = Field(default=None, ge=0)


class ProductRequest(BaseModel):
    product_id: str = Field(min_length=1)


class ProductCompareRequest(BaseModel):
    product_ids: list[str] = Field(min_length=2)


class OrderRequest(BaseModel):
    order_id: str = Field(min_length=1)


class CreateOrderRequest(BaseModel):
    customer_id: str
    product_id: str
    quantity: int = Field(gt=0, le=20)


class UpdateOrderRequest(BaseModel):
    order_id: str
    update_data: dict[str, Any]


class CustomerRequest(BaseModel):
    customer_id: str


class UpdateCustomerRequest(BaseModel):
    customer_id: str
    update_data: dict[str, Any]


class ReturnRequest(BaseModel):
    order_id: str
    reason: str = Field(min_length=3)


class ReturnStatusRequest(BaseModel):
    return_id: str


class QueryRequest(BaseModel):
    query: str = Field(min_length=1)
