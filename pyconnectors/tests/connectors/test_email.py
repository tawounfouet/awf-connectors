import pytest
from unittest.mock import MagicMock, patch

from pyconnectors.config import ConnectorConfig
from pyconnectors.connectors.email.brevo import BrevoConnector
from pyconnectors.connectors.email.gmail import GmailConnector
from pyconnectors.connectors.email.imap import IMAPConnector
from pyconnectors.connectors.email.mailchimp import MailchimpConnector
from pyconnectors.connectors.email.mailersend import MailerSendConnector
from pyconnectors.connectors.email.mailgun import MailgunConnector
from pyconnectors.connectors.email.outlook import OutlookConnector
from pyconnectors.connectors.email.pop3 import POP3Connector
from pyconnectors.connectors.email.resend import ResendConnector
from pyconnectors.connectors.email.ses import SESConnector
from pyconnectors.connectors.email.smtp import SMTPConnector
from pyconnectors.connectors.email.yahoo import YahooConnector


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


@patch("imaplib.IMAP4_SSL")
def test_imap_connector_execute(mock_imap):
    config = ConnectorConfig(params={"host": "imap.example.com", "user": "user", "password": "pwd"})
    connector = IMAPConnector(config)

    mock_mail = MagicMock()
    mock_imap.return_value = mock_mail
    mock_mail.search.return_value = ("OK", [b"1 2 3"])

    result = connector.execute("INBOX", "list", "ALL")

    assert result["status"] == "success"
    assert result["count"] == 3
    assert result["messages"] == ["1", "2", "3"]

    mock_imap.assert_called_with("imap.example.com", 993)
    mock_mail.login.assert_called_with("user", "pwd")
    mock_mail.select.assert_called_with("INBOX")
    mock_mail.search.assert_called_with(None, "ALL")


@patch("poplib.POP3_SSL")
def test_pop3_connector_execute(mock_pop3):
    config = ConnectorConfig(params={"host": "pop.example.com", "user": "user", "password": "pwd"})
    connector = POP3Connector(config)

    mock_mail = MagicMock()
    mock_pop3.return_value = mock_mail
    mock_mail.stat.return_value = (5, 1024)

    result = connector.execute("stat")

    assert result["status"] == "success"
    assert result["count"] == 5
    assert result["size"] == 1024

    mock_pop3.assert_called_with("pop.example.com", 995)
    mock_mail.user.assert_called_with("user")
    mock_mail.pass_.assert_called_with("pwd")
    mock_mail.stat.assert_called_with()


@patch("smtplib.SMTP")
def test_gmail_connector_execute(mock_smtp):
    config = ConnectorConfig(params={"user": "test@gmail.com", "password": "pwd"})
    connector = GmailConnector(config)

    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    result = connector.execute("recipient@example.com", "Subject", "Body")
    assert result["status"] == "sent"
    mock_smtp.assert_called_with("smtp.gmail.com", 587)
    mock_server.starttls.assert_called_with()


@patch("smtplib.SMTP")
def test_outlook_connector_execute(mock_smtp):
    config = ConnectorConfig(params={"user": "test@outlook.com", "password": "pwd"})
    connector = OutlookConnector(config)

    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    result = connector.execute("recipient@example.com", "Subject", "Body")
    assert result["status"] == "sent"
    mock_smtp.assert_called_with("smtp-mail.outlook.com", 587)


@patch("smtplib.SMTP_SSL")
def test_yahoo_connector_execute(mock_smtp_ssl):
    config = ConnectorConfig(params={"user": "test@yahoo.com", "password": "pwd"})
    connector = YahooConnector(config)

    mock_server = MagicMock()
    mock_smtp_ssl.return_value.__enter__.return_value = mock_server

    result = connector.execute("recipient@example.com", "Subject", "Body")
    assert result["status"] == "sent"
    mock_smtp_ssl.assert_called_with("smtp.mail.yahoo.com", 465)


@patch("urllib.request.urlopen")
def test_resend_connector_execute(mock_urlopen):
    config = ConnectorConfig(params={"api_key": "res_key", "from_addr": "info@me.com"})
    connector = ResendConnector(config)

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value = b'{"id": "em_123"}'
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_context

    result = connector.execute("to@you.com", "Test", "<p>HTML</p>")
    assert result["status"] == 200
    assert result["data"]["id"] == "em_123"


@patch("urllib.request.urlopen")
def test_brevo_connector_execute(mock_urlopen):
    config = ConnectorConfig(params={"api_key": "br_key", "from_addr": "info@me.com"})
    connector = BrevoConnector(config)

    mock_response = MagicMock()
    mock_response.status = 201
    mock_response.read.return_value = b'{"messageId": "br_123"}'
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_context

    result = connector.execute("to@you.com", "Test", "<p>HTML</p>")
    assert result["status"] == 201
    assert result["data"]["messageId"] == "br_123"


@patch("urllib.request.urlopen")
def test_mailchimp_connector_execute(mock_urlopen):
    config = ConnectorConfig(params={"api_key": "mc_key", "from_addr": "info@me.com"})
    connector = MailchimpConnector(config)

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value = b'[{"status": "sent", "_id": "mc_123"}]'
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_context

    result = connector.execute("to@you.com", "Test", "<p>HTML</p>", "Me")
    assert result["status"] == 200
    assert result["data"][0]["_id"] == "mc_123"


@patch("urllib.request.urlopen")
def test_mailersend_connector_execute(mock_urlopen):
    config = ConnectorConfig(params={"api_key": "ms_key", "from_addr": "info@me.com"})
    connector = MailerSendConnector(config)

    mock_response = MagicMock()
    mock_response.status = 202
    mock_response.read.return_value = b""
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_context

    result = connector.execute("to@you.com", "Test", "<p>HTML</p>")
    assert result["status"] == 202


@patch("urllib.request.urlopen")
def test_mailgun_connector_execute(mock_urlopen):
    config = ConnectorConfig(
        params={"api_key": "mg_key", "domain": "mg.me.com", "from_addr": "info@me.com"}
    )
    connector = MailgunConnector(config)

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value = b'{"id": "mg_123", "message": "Queued"}'
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_context

    result = connector.execute("to@you.com", "Test", "<p>HTML</p>")
    assert result["status"] == 200
    assert result["data"]["id"] == "mg_123"


@patch("pyconnectors.connectors.email.ses.boto3")
def test_ses_connector_execute(mock_boto3):
    if mock_boto3 is None:
        pytest.skip("boto3 not available")

    config = ConnectorConfig(
        params={
            "from_addr": "info@me.com",
            "aws_access_key_id": "key",
            "aws_secret_access_key": "secret",
        }
    )
    connector = SESConnector(config)

    mock_client = MagicMock()
    mock_boto3.client.return_value = mock_client
    mock_client.send_email.return_value = {"MessageId": "ses_123"}

    result = connector.execute("to@you.com", "Subject", "<p>HTML</p>")

    assert result["status"] == "sent"
    assert result["message_id"] == "ses_123"
    mock_boto3.client.assert_called_with(
        "ses",
        aws_access_key_id="key",
        aws_secret_access_key="secret",
        region_name="us-east-1",
    )
