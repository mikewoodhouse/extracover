import sqlite3
from pathlib import Path
from typing import Protocol


class Database(Protocol):
    def query_result(self, sql: str, params: dict | None = None) -> list[dict]:
        raise NotImplementedError


class SQLiteDatabase:
    def __init__(self, path: Path) -> None:
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row

    def query_result(self, sql: str, params: dict | None = None) -> list[dict]:
        params = params or {}
        return list(dict(row) for row in self.conn.execute(sql, params).fetchall())
