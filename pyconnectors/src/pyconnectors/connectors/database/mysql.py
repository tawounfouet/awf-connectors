from typing import Any

from pyconnectors.base import BaseConnector
from pyconnectors.registry import connector

try:
    import pymysql  # type: ignore
except ImportError:
    pymysql = None


@connector("database.mysql")
class MySQLConnector(BaseConnector):
    """MySQL Connector using pymysql."""

    def execute(self, query: str, params: tuple[Any, ...] | None = None) -> list[Any]:
        if pymysql is None:
            raise ImportError(
                "MySQL connector requires pymysql. Install with: pip install pyconnectors[mysql]"
            )

        host = self.config.params.get("host", "localhost")
        port = self.config.params.get("port", 3306)
        user = self.config.params.get("user")
        password = self.config.params.get("password")
        database = self.config.params.get("database")

        if not all([user, password, database]):
            raise ValueError("Configuration missing 'user', 'password', or 'database' parameters.")

        with pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor,
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return list(cur.fetchall())
