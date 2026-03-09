import pytest
from unittest.mock import MagicMock, patch

from pyconnectors.config import ConnectorConfig
from pyconnectors.connectors.email.smtp import SMTPConnector


@pytest.fixture
def smtp_connector():
    config = ConnectorConfig(
        params={
            "host": "smtp.example.com",
            "port": 587,
            "user": "test_user",
            "password": "test_password",
            "from_addr": "test@example.com",
        }
    )
    return SMTPConnector(config)


@patch("smtplib.SMTP")
def test_smtp_connector_execute(mock_smtp, smtp_connector):
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    result = smtp_connector.execute("recipient@example.com", "Test Subject", "Test Body")

    assert result == {"status": "sent"}

    # Verify SMTP calls
    mock_smtp.assert_called_with("smtp.example.com", 587)
    mock_server.login.assert_called_with("test_user", "test_password")

    # Verify message
    call_args = mock_server.send_message.call_args[0]
    msg = call_args[0]
    assert msg["Subject"] == "Test Subject"
    assert msg["From"] == "test@example.com"
    assert msg["To"] == "recipient@example.com"
