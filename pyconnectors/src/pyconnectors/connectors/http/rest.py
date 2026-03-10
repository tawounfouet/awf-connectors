from typing import Any
from pyconnectors.base import BaseConnector
from pyconnectors.registry import connector

try:
    import urllib.request
    import json
except ImportError:
    pass


@connector("http.rest")
class RestConnector(BaseConnector):
    """Minimal REST API Connector using stdlib urllib."""

    def execute(
        self,
        method: str,
        url: str,
        data: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        req_headers = headers or {}
        if "Content-Type" not in req_headers:
            req_headers["Content-Type"] = "application/json"

        req_data = None
        if data:
            req_data = json.dumps(data).encode("utf-8")

        req = urllib.request.Request(url, data=req_data, headers=req_headers, method=method.upper())
        with urllib.request.urlopen(req) as response:
            return {"status": response.status, "body": response.read().decode("utf-8")}
