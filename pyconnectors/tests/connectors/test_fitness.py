import pytest
from unittest.mock import MagicMock, patch

from pyconnectors.config import ConnectorConfig
from pyconnectors.connectors.fitness.strava import StravaConnector


@patch("urllib.request.urlopen")
def test_strava_connector_execute_get(mock_urlopen):
    config = ConnectorConfig(params={"access_token": "strava_token"})
    connector = StravaConnector(config)

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value = b'[{"id": 123, "name": "Morning Run"}]'
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_context

    result = connector.execute("athlete/activities", data={"per_page": 2})

    assert result["status"] == 200
    assert result["data"][0]["name"] == "Morning Run"

    req = mock_urlopen.call_args[0][0]
    # Check that URL has query params properly appended
    assert "https://www.strava.com/api/v3/athlete/activities?per_page=2" in req.full_url
    assert req.get_method() == "GET"
    assert req.get_header("Authorization") == "Bearer strava_token"


@patch("urllib.request.urlopen")
def test_strava_connector_execute_post(mock_urlopen):
    config = ConnectorConfig(params={"access_token": "strava_token"})
    connector = StravaConnector(config)

    mock_response = MagicMock()
    mock_response.status = 201
    mock_response.read.return_value = b'{"id": 456, "name": "New Ride"}'
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_context

    payload = {"name": "New Ride", "type": "Ride", "sport_type": "Ride"}
    result = connector.execute("activities", data=payload, method="POST")

    assert result["status"] == 201
    assert result["data"]["id"] == 456

    req = mock_urlopen.call_args[0][0]
    assert req.full_url == "https://www.strava.com/api/v3/activities"
    assert req.get_method() == "POST"
    assert req.get_header("Authorization") == "Bearer strava_token"
    assert req.get_header("Content-type") == "application/json"
