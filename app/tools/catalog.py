"""Build the default registry with all real demo tools."""
from .base import RegisteredTool, ToolMetadata
from .registry import ToolRegistry, generate_mock_tools
from .product_tools import search_products, get_product_details, check_product_stock, compare_products
from .order_tools import create_order, get_order, cancel_order, update_order
from .customer_tools import get_customer, update_customer
from .delivery_tools import track_order, get_delivery_status
from .payment_tools import get_payment_status, refund_payment
from .return_tools import create_return, get_return_status
from .rag_tool import rag_search
from .system_search_tool import system_search


def build_registry(include_simulated: int = 1000) -> ToolRegistry:
    registry = ToolRegistry()
    definitions = [
        ("search_products", "Search products by name, category, and price", "product", "search", ["query"], ["max_price"], "product:read", search_products),
        ("get_product_details", "Get product details", "product", "read", ["product_id"], [], "product:read", get_product_details),
        ("check_product_stock", "Check product stock", "product", "stock", ["product_id"], [], "product:read", check_product_stock),
        ("compare_products", "Compare products by rating and price", "product", "compare", ["product_ids"], [], "product:read", compare_products),
        ("create_order", "Create an order", "order", "create", ["customer_id", "product_id", "quantity"], [], "order:create", create_order),
        ("get_order", "Get an order", "order", "read", ["order_id"], [], "order:read", get_order),
        ("cancel_order", "Cancel an order", "order", "cancel", ["order_id"], [], "order:cancel", cancel_order),
        ("update_order", "Update an order", "order", "update", ["order_id", "update_data"], [], "order:update", update_order),
        ("get_customer", "Get customer profile", "customer", "read", ["customer_id"], [], "customer:read", get_customer),
        ("update_customer", "Update customer profile", "customer", "update", ["customer_id", "update_data"], [], "customer:update", update_customer),
        ("track_order", "Track delivery status of an order", "delivery", "track", ["order_id"], [], "delivery:read", track_order),
        ("get_delivery_status", "Get delivery status", "delivery", "status", ["order_id"], [], "delivery:read", get_delivery_status),
        ("get_payment_status", "Get payment status", "payment", "status", ["order_id"], [], "payment:read", get_payment_status),
        ("refund_payment", "Refund a payment", "payment", "refund", ["order_id"], [], "payment:refund", refund_payment),
        ("create_return", "Create a product return", "return", "create", ["order_id", "reason"], [], "return:create", create_return),
        ("get_return_status", "Get return status", "return", "status", ["return_id"], [], "return:read", get_return_status),
        ("rag_search", "Search the shopping knowledge base", "knowledge", "retrieve", ["query"], [], "knowledge:read", rag_search),
        ("system_search", "Search tools and request history", "system", "search", ["query"], [], "system:read", lambda query: {"query": query}),
    ]
    for name, description, domain, operation, required, optional, permission, handler in definitions:
        registry.register_tool(RegisteredTool(ToolMetadata(name, description, domain, operation, required, optional, permission=permission), handler))
    if include_simulated:
        generate_mock_tools(registry, include_simulated)
    return registry
