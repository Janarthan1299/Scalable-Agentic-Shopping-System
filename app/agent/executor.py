"""Tool Gateway: permission, validation, retry, execution, and audit."""
import logging
import time
from typing import Any
from app.services.permission_service import PermissionService
from app.services.validator import ParameterValidator
from app.services.audit_service import AuditService
from app.tools.registry import ToolRegistry
from app.utils.retry import with_retry

logger = logging.getLogger(__name__)


class ToolGateway:
    def __init__(self, registry: ToolRegistry, audit: AuditService, permissions: PermissionService | None = None, validator: ParameterValidator | None = None, max_retries: int = 2) -> None:
        self.registry, self.audit = registry, audit
        self.permissions = permissions or PermissionService()
        self.validator = validator or ParameterValidator()
        self.max_retries = max_retries

    def execute(self, request_id: str, user_id: str, tool_name: str, parameters: dict[str, Any]) -> dict[str, Any]:
        started = time.perf_counter()
        status = "success"
        try:
            tool = self.registry.get_tool(tool_name)
            self.permissions.check(user_id, tool.metadata.permission)
            clean_parameters = self.validator.validate(tool_name, parameters)
            result = with_retry(lambda: tool.invoke(clean_parameters), self.max_retries)
            return result
        except Exception as exc:
            status = "error"
            result = {"error": str(exc), "tool": tool_name}
            raise
        finally:
            duration = time.perf_counter() - started
            if "result" in locals():
                self.audit.execution(request_id, tool_name, parameters, result, status, duration)
            logger.info("request_id=%s tool=%s status=%s duration_ms=%.2f", request_id, tool_name, status, duration * 1000)
