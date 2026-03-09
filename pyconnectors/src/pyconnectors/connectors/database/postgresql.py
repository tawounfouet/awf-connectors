from typing import Any
from pyconnectors.base import BaseConnector
from pyconnectors.registry import connector

try:
    import psycopg
except ImportError:
    psycopg = None


@connector("database.postgresql")
class PostgreSQLConnector(BaseConnector):
    """PostgreSQL Connector using psycopg."""

    def execute(self, query: str, params: tuple[Any, ...] | None = None) -> list[Any]:
        if psycopg is None:
            raise ImportError(
                "PostgreSQL connector requires psycopg. Install with: pip install pyconnectors[postgresql]"
            )

        dsn = self.config.params.get("dsn")
        if not dsn:
            raise ValueError("Configuration missing 'dsn' parameter.")

        with psycopg.connect(dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                try:
                    return list(cur.fetchall())
                except psycopg.ProgrammingError:
                    # e.g., for INSERT/UPDATE without RETURNING
                    return []
