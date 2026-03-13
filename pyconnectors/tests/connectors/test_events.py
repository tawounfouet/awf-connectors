import pytest
from unittest.mock import MagicMock, patch

from pyconnectors.config import ConnectorConfig
from pyconnectors.connectors.events.eventbrite import EventbriteConnector


@patch("urllib.request.urlopen")
def test_eventbrite_connector_execute_get(mock_urlopen):
    config = ConnectorConfig(params={"private_token": "eb_token"})
    connector = EventbriteConnector(config)

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value = b'{"events": [{"name": "My Event"}]}'
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_context

    result = connector.execute("users/me/events", data={"status": "live"})

    assert result["status"] == 200
    assert result["data"]["events"][0]["name"] == "My Event"

    req = mock_urlopen.call_args[0][0]
    assert "https://www.eventbriteapi.com/v3/users/me/events?status=live" in req.full_url
    assert req.get_method() == "GET"
    assert req.get_header("Authorization") == "Bearer eb_token"


@patch("urllib.request.urlopen")
def test_eventbrite_connector_execute_post(mock_urlopen):
    config = ConnectorConfig(params={"private_token": "eb_token"})
    connector = EventbriteConnector(config)

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value = b'{"id": "123"}'
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_context

    result = connector.execute("events/123/", data={"event": {}}, method="POST")

    assert result["status"] == 200
    assert result["data"]["id"] == "123"

    req = mock_urlopen.call_args[0][0]
    assert req.full_url == "https://www.eventbriteapi.com/v3/events/123/"
    assert req.get_method() == "POST"
    assert req.get_header("Authorization") == "Bearer eb_token"
    assert req.get_header("Content-type") == "application/json"
