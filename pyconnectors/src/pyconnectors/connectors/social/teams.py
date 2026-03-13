import json
import urllib.request
from typing import Any

from pyconnectors.base import BaseConnector
from pyconnectors.registry import connector


@connector("social.teams")
class TeamsConnector(BaseConnector):
    """Microsoft Teams Webhook Connector."""

    def execute(
        self, text: str, title: str | None = None, theme_color: str | None = None
    ) -> dict[str, Any]:
        webhook_url = self.config.params.get("webhook_url")
        if not webhook_url:
            raise ValueError("TeamsConnector requires 'webhook_url' in configuration.")

        payload: dict[str, Any] = {"text": text}

        if title:
            payload["title"] = title
        if theme_color:
            payload["themeColor"] = theme_color

        req_data = json.dumps(payload).encode("utf-8")

        req = urllib.request.Request(
            webhook_url,
            data=req_data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req) as response:
                return {"status": response.status}
        except urllib.error.HTTPError as e:
            return {"status": e.code, "error": e.read().decode("utf-8")}
