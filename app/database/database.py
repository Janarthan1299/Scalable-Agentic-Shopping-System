"""Small SQLite store for requests, tools, users, and executions."""
import json
import sqlite3
from pathlib import Path
from typing import Any


class Database:
    def __init__(self, path: str = "shopping_agent.db") -> None:
        self.memory = path == ":memory:"
        self.path = Path(path.replace("sqlite:///./", "")) if not self.memory else Path("shopping_agent_memory.db")
        self._memory_connection = sqlite3.connect(":memory:") if self.memory else None
        if self._memory_connection:
            self._memory_connection.row_factory = sqlite3.Row
        self.initialize()

    def connect(self) -> sqlite3.Connection:
        if self._memory_connection:
            return self._memory_connection
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self) -> None:
        with self.connect() as db:
            db.executescript("""
            CREATE TABLE IF NOT EXISTS tools (id INTEGER PRIMARY KEY, name TEXT UNIQUE, description TEXT, domain TEXT, operation TEXT, permission TEXT, risk_level TEXT, version TEXT, enabled INTEGER);
            CREATE TABLE IF NOT EXISTS requests (id TEXT PRIMARY KEY, user_id TEXT, query TEXT, intent TEXT, domain TEXT, status TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS tool_executions (id INTEGER PRIMARY KEY, request_id TEXT, tool_name TEXT, parameters TEXT, result TEXT, status TEXT, duration REAL, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, role TEXT);
            """)

    def save_request(self, request_id: str, user_id: str, query: str, intent: str, domain: str, status: str) -> None:
        with self.connect() as db:
            db.execute("INSERT OR REPLACE INTO requests(id,user_id,query,intent,domain,status) VALUES(?,?,?,?,?,?)", (request_id, user_id, query, intent, domain, status))

    def save_execution(self, request_id: str, tool_name: str, parameters: dict[str, Any], result: Any, status: str, duration: float) -> None:
        with self.connect() as db:
            db.execute("INSERT INTO tool_executions(request_id,tool_name,parameters,result,status,duration) VALUES(?,?,?,?,?,?)", (request_id, tool_name, json.dumps(parameters), json.dumps(result, default=str), status, duration))

    def get_request(self, request_id: str) -> dict[str, Any] | None:
        with self.connect() as db:
            row = db.execute("SELECT * FROM requests WHERE id=?", (request_id,)).fetchone()
            return dict(row) if row else None

    def search_history(self, query: str) -> list[dict[str, Any]]:
        with self.connect() as db:
            rows = db.execute("SELECT * FROM requests WHERE query LIKE ? ORDER BY created_at DESC LIMIT 10", (f"%{query}%",)).fetchall()
            return [dict(row) for row in rows]
