import json
import urllib.parse
import urllib.request
from typing import Any

from pyconnectors.base import BaseConnector
from pyconnectors.registry import connector


@connector("payment.helloasso")
class HelloAssoConnector(BaseConnector):
    """HelloAsso API Connector handling Client Credentials natively."""

    def execute(
        self, endpoint: str, data: dict[str, Any] | None = None, method: str = "GET"
    ) -> dict[str, Any]:
        client_id = self.config.params.get("client_id")
        client_secret = self.config.params.get("client_secret")

        if not all([client_id, client_secret]):
            raise ValueError("HelloAssoConnector requires 'client_id' and 'client_secret'.")

        base_url = "https://api.helloasso.com/v5"

        # 1. Get OAuth2 Token
        token_payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        }
        token_req = urllib.request.Request(
            f"{base_url}/oauth2/token",
            data=urllib.parse.urlencode(token_payload).encode("utf-8"),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(token_req) as token_res:
                token_data = json.loads(token_res.read().decode("utf-8"))
                access_token = token_data.get("access_token")
        except urllib.error.HTTPError as e:
            return {"status": "error", "error": f"Auth failed: {e.read().decode('utf-8')}"}

        # 2. Make Actual API request
        url = f"{base_url}/{endpoint.lstrip('/')}"

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

        api_req = urllib.request.Request(
            url,
            data=req_data,
            headers=headers,
            method=method.upper(),
        )

        try:
            with urllib.request.urlopen(api_req) as response:
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
