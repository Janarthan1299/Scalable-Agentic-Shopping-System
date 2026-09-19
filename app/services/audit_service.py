"""Request and execution audit facade."""
from app.database.database import Database


class AuditService:
    def __init__(self, database: Database) -> None:
        self.database = database

    def request(self, request_id: str, user_id: str, query: str, intent: str, domain: str, status: str = "running") -> None:
        self.database.save_request(request_id, user_id, query, intent, domain, status)

    def execution(self, request_id: str, tool_name: str, parameters: dict, result: object, status: str, duration: float) -> None:
        self.database.save_execution(request_id, tool_name, parameters, result, status, duration)
