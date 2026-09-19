"""Role-based permission checks for the tool gateway."""
class PermissionDenied(Exception):
    pass


ROLE_PERMISSIONS = {
    "customer": {"product:read", "order:read", "order:create", "order:cancel", "delivery:read", "payment:read", "return:create", "return:read", "knowledge:read", "system:read"},
    "support_agent": {"product:read", "order:read", "order:update", "order:cancel", "delivery:read", "payment:read", "payment:refund", "return:create", "return:read", "customer:read", "customer:update", "knowledge:read", "system:read"},
    "admin": {"*"},
}


class PermissionService:
    def __init__(self) -> None:
        self.roles = {"C001": "customer", "C002": "customer", "C003": "customer", "SUPPORT": "support_agent", "ADMIN": "admin"}

    def check(self, user_id: str, permission: str) -> None:
        role = self.roles.get(user_id, "customer")
        allowed = ROLE_PERMISSIONS[role]
        if "*" not in allowed and permission not in allowed:
            raise PermissionDenied(f"Role {role} lacks permission {permission}")
