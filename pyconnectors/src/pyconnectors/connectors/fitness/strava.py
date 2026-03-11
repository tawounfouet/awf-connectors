import json
import urllib.parse
import urllib.request
from typing import Any

from pyconnectors.base import BaseConnector
from pyconnectors.registry import connector


@connector("fitness.strava")
class StravaConnector(BaseConnector):
    """Strava API Connector using stdlib. Requires OAuth2 tokens."""

    def execute(
        self, endpoint: str, data: dict[str, Any] | None = None, method: str = "GET"
    ) -> dict[str, Any]:
        access_token = self.config.params.get("access_token")
        if not access_token:
            raise ValueError("StravaConnector requires 'access_token' in configuration.")

        base_url = "https://www.strava.com/api/v3"
        url = f"{base_url}/{endpoint.lstrip('/')}"

        # If data is provided for GET, convert to query params
        if method.upper() == "GET" and data:
            query = urllib.parse.urlencode(data)
            url = f"{url}?{query}"
            req_data = None
        else:
            req_data = json.dumps(data).encode("utf-8") if data else None

        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        if req_data:
            headers["Content-Type"] = "application/json"

        req = urllib.request.Request(
            url,
            data=req_data,
            headers=headers,
            method=method.upper(),
        )

        try:
            with urllib.request.urlopen(req) as response:
                response_body = response.read().decode("utf-8")
                return {
                    "status": response.status,
                    "data": json.loads(response_body) if response_body else {},
                }
        except urllib.error.HTTPError as e:
            return {
                "status": e.code,
                "error": json.loads(e.read().decode("utf-8")) if e.read() else str(e),
            }
