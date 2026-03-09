import json
import pytest
from unittest.mock import MagicMock, patch

from pyconnectors.config import ConnectorConfig
from pyconnectors.connectors.social.slack import SlackConnector


@pytest.fixture
def slack_connector():
    config = ConnectorConfig(params={"webhook_url": "https://hooks.slack.com/services/T/B/X"})
    return SlackConnector(config)


@patch("urllib.request.urlopen")
def test_slack_connector_execute(mock_urlopen, slack_connector):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_context

    result = slack_connector.execute("Hello from PyConnectors!", channel="#general")

    assert result == {"status": 200}

    req = mock_urlopen.call_args[0][0]
    assert req.full_url == "https://hooks.slack.com/services/T/B/X"
    assert req.get_method() == "POST"

    payload = json.loads(req.data.decode("utf-8"))
    assert payload["text"] == "Hello from PyConnectors!"
    assert payload["channel"] == "#general"


def test_slack_connector_no_webhook():
    config = ConnectorConfig()
    connector = SlackConnector(config)
    with pytest.raises(ValueError):
        connector.execute("test")
