"""Seed registry metadata and demo users into SQLite."""
from app.database.database import Database
from app.tools.registry import ToolRegistry


def seed_database(db: Database, registry: ToolRegistry) -> None:
    with db.connect() as connection:
        for tool in registry.list_tools():
            metadata = tool.metadata
            connection.execute("INSERT OR REPLACE INTO tools(name,description,domain,operation,permission,risk_level,version,enabled) VALUES(?,?,?,?,?,?,?,?)", (metadata.name, metadata.description, metadata.domain, metadata.operation, metadata.permission, metadata.risk_level, metadata.version, int(metadata.enabled)))
        for user_id, role in (("C001", "customer"), ("C002", "customer"), ("SUPPORT", "support_agent"), ("ADMIN", "admin")):
            connection.execute("INSERT OR REPLACE INTO users(id,role) VALUES(?,?)", (user_id, role))
