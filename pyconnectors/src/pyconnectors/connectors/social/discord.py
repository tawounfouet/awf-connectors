import json
import urllib.request
from typing import Any

from pyconnectors.base import BaseConnector
from pyconnectors.registry import connector


@connector("social.discord")
class DiscordConnector(BaseConnector):
    """Discord Webhook Connector."""

    def execute(
        self,
        content: str,
        username: str | None = None,
        avatar_url: str | None = None,
        embeds: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        webhook_url = self.config.params.get("webhook_url")
        if not webhook_url:
            raise ValueError("DiscordConnector requires 'webhook_url' in configuration.")

        payload: dict[str, Any] = {"content": content}

        if username:
            payload["username"] = username
        if avatar_url:
            payload["avatar_url"] = avatar_url
        if embeds:
            payload["embeds"] = embeds

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
