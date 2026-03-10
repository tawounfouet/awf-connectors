import sqlite3
from typing import Any

from pyconnectors.base import BaseConnector
from pyconnectors.registry import connector


@connector("database.sqlite")
class SQLiteConnector(BaseConnector):
    """SQLite Connector using stdlib sqlite3."""

    def execute(self, query: str, params: tuple[Any, ...] | None = None) -> list[Any]:
        database = self.config.params.get("database", ":memory:")

        with sqlite3.connect(database) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(query, params or ())

            try:
                # Convert rows to dicts for easier consumption
                return [dict(row) for row in cur.fetchall()]
            except sqlite3.ProgrammingError:
                # e.g., for INSERT/UPDATE without returning rows
                return []
