import json
import pytest
from unittest.mock import MagicMock, patch

from pyconnectors.config import ConnectorConfig
from pyconnectors.connectors.social.facebook import FacebookConnector
from pyconnectors.connectors.social.instagram import InstagramConnector
from pyconnectors.connectors.social.linkedin import LinkedInConnector
from pyconnectors.connectors.social.slack import SlackConnector
from pyconnectors.connectors.social.tiktok import TikTokConnector
from pyconnectors.connectors.social.twitter import TwitterConnector


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


@patch("urllib.request.urlopen")
def test_facebook_connector_execute(mock_urlopen):
    config = ConnectorConfig(params={"access_token": "fb_token"})
    connector = FacebookConnector(config)

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value = b'{"id": "123"}'
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_context

    result = connector.execute("me")

    assert result["status"] == 200
    assert result["data"] == {"id": "123"}

    req = mock_urlopen.call_args[0][0]
    assert req.full_url == "https://graph.facebook.com/v19.0/me?access_token=fb_token"


@patch("urllib.request.urlopen")
def test_linkedin_connector_execute(mock_urlopen):
    config = ConnectorConfig(params={"access_token": "li_token"})
    connector = LinkedInConnector(config)

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value = b'{"localizedFirstName": "Jules"}'
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_context

    result = connector.execute("me")

    assert result["status"] == 200
    assert result["data"] == {"localizedFirstName": "Jules"}

    req = mock_urlopen.call_args[0][0]
    assert req.full_url == "https://api.linkedin.com/v2/me"
    assert req.get_header("Authorization") == "Bearer li_token"


@patch("urllib.request.urlopen")
def test_twitter_connector_execute(mock_urlopen):
    config = ConnectorConfig(params={"bearer_token": "tw_token"})
    connector = TwitterConnector(config)

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value = b'{"data": []}'
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_context

    result = connector.execute("users/me")

    assert result["status"] == 200
    assert result["data"] == {"data": []}

    req = mock_urlopen.call_args[0][0]
    assert req.full_url == "https://api.twitter.com/2/users/me"
    assert req.get_header("Authorization") == "Bearer tw_token"


@patch("urllib.request.urlopen")
def test_tiktok_connector_execute(mock_urlopen):
    config = ConnectorConfig(params={"access_token": "tk_token"})
    connector = TikTokConnector(config)

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value = b'{"data": {}}'
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_context

    result = connector.execute("user/info/")

    assert result["status"] == 200
    assert result["data"] == {"data": {}}

    req = mock_urlopen.call_args[0][0]
    assert req.full_url == "https://open.tiktokapis.com/v2/user/info/"
    assert req.get_header("Authorization") == "Bearer tk_token"


@patch("urllib.request.urlopen")
def test_instagram_connector_execute(mock_urlopen):
    config = ConnectorConfig(params={"access_token": "ig_token"})
    connector = InstagramConnector(config)

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value = b'{"id": "456"}'
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_context

    result = connector.execute("me/media")

    assert result["status"] == 200
    assert result["data"] == {"id": "456"}

    req = mock_urlopen.call_args[0][0]
    assert req.full_url == "https://graph.instagram.com/v19.0/me/media?access_token=ig_token"
