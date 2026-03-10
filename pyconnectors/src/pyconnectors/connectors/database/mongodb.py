from typing import Any

from pyconnectors.base import BaseConnector
from pyconnectors.registry import connector

try:
    import pymongo
except ImportError:
    pymongo = None


@connector("database.mongodb")
class MongoDBConnector(BaseConnector):
    """MongoDB Connector using pymongo."""

    def execute(
        self,
        collection: str,
        action: str,
        query: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        if pymongo is None:
            raise ImportError(
                "MongoDB connector requires pymongo. Install with: pip install pyconnectors[mongodb]"
            )

        uri = self.config.params.get("uri")
        database = self.config.params.get("database")

        if not uri or not database:
            raise ValueError("Configuration missing 'uri' or 'database' parameters.")

        client: Any = pymongo.MongoClient(uri)
        db = client[database]
        col = db[collection]

        try:
            if action == "find":
                return list(col.find(query or {}))
            elif action == "find_one":
                return col.find_one(query or {})
            elif action == "insert_one":
                result = col.insert_one(data or {})
                return {"inserted_id": str(result.inserted_id)}
            else:
                raise ValueError(f"Action '{action}' is not supported by MongoDBConnector.")
        finally:
            client.close()
