import pytest
from unittest.mock import MagicMock, patch

from pyconnectors.config import ConnectorConfig
from pyconnectors.connectors.crm.hubspot import HubSpotConnector


@patch("urllib.request.urlopen")
def test_hubspot_connector_execute_get(mock_urlopen):
    config = ConnectorConfig(params={"access_token": "hs_token"})
    connector = HubSpotConnector(config)

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value = b'{"results": [{"id": "123"}]}'
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_context

    result = connector.execute("crm/v3/objects/contacts", data={"limit": 10})

    assert result["status"] == 200
    assert result["data"]["results"][0]["id"] == "123"

    req = mock_urlopen.call_args[0][0]
    assert "https://api.hubapi.com/crm/v3/objects/contacts?limit=10" in req.full_url
    assert req.get_method() == "GET"
    assert req.get_header("Authorization") == "Bearer hs_token"


@patch("urllib.request.urlopen")
def test_hubspot_connector_execute_post(mock_urlopen):
    config = ConnectorConfig(params={"access_token": "hs_token"})
    connector = HubSpotConnector(config)

    mock_response = MagicMock()
    mock_response.status = 201
    mock_response.read.return_value = b'{"id": "456"}'
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_context

    payload = {"properties": {"email": "test@example.com"}}
    result = connector.execute("crm/v3/objects/contacts", data=payload, method="POST")

    assert result["status"] == 201
    assert result["data"]["id"] == "456"

    req = mock_urlopen.call_args[0][0]
    assert req.full_url == "https://api.hubapi.com/crm/v3/objects/contacts"
    assert req.get_method() == "POST"
    assert req.get_header("Authorization") == "Bearer hs_token"
    assert req.get_header("Content-type") == "application/json"
