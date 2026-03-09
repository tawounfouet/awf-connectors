import pytest
from unittest.mock import MagicMock, patch
from pyconnectors.config import ConnectorConfig
from pyconnectors.connectors.http.rest import RestConnector


@pytest.fixture
def http_connector():
    config = ConnectorConfig()
    return RestConnector(config)


@patch("urllib.request.urlopen")
def test_http_rest_execute(mock_urlopen, http_connector):
    # Setup mock
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value = b'{"hello": "world"}'

    # Enter context manager
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_context

    result = http_connector.execute("GET", "http://example.com/api")

    assert result["status"] == 200
    assert result["body"] == '{"hello": "world"}'

    # Verify urllib call
    req = mock_urlopen.call_args[0][0]
    assert req.get_method() == "GET"
    assert req.full_url == "http://example.com/api"
    assert req.get_header("Content-type") == "application/json"
