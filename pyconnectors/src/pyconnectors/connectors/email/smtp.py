from typing import Any
from pyconnectors.base import BaseConnector
from pyconnectors.registry import connector

try:
    import smtplib
    from email.mime.text import MIMEText
except ImportError:
    pass


@connector("email.smtp")
class SMTPConnector(BaseConnector):
    """SMTP Email Connector."""

    def execute(self, to_addr: str, subject: str, body: str) -> dict[str, Any]:
        host = self.config.params.get("host", "localhost")
        port = self.config.params.get("port", 25)
        user = self.config.params.get("user")
        password = self.config.params.get("password")
        from_addr = self.config.params.get("from_addr", "no-reply@localhost")

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = to_addr

        with smtplib.SMTP(host, port) as server:
            if user and password:
                server.login(user, password)
            server.send_message(msg)

        return {"status": "sent"}
