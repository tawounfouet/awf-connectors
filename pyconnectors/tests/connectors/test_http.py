import pytest
from unittest.mock import MagicMock, patch
from pyconnectors.config import ConnectorConfig
from pyconnectors.connectors.http.rest import RestConnector


@pytest.fixture
def mock_response():
    resp = MagicMock()
    resp.status = 200
    resp.read.return_value = b'{"hello": "world"}'
    context = MagicMock()
    context.__enter__.return_value = resp
    return context


def test_http_rest_execute(mock_response):
    config = ConnectorConfig()
    with patch("urllib.request.build_opener") as mock_build_opener:
        mock_opener = MagicMock()
        mock_opener.open.return_value = mock_response
        mock_build_opener.return_value = mock_opener

        http_connector = RestConnector(config)
        result = http_connector.execute("GET", "http://example.com/api")

        assert result["status"] == 200
        assert result["body"] == '{"hello": "world"}'

        req = mock_opener.open.call_args[0][0]
        assert req.get_method() == "GET"
        assert req.full_url == "http://example.com/api"
        assert req.get_header("Content-type") == "application/json"


def test_http_rest_api_key_header(mock_response):
    config = ConnectorConfig(
        params={
            "api_key": "mysecret",
            "api_key_header": "X-API-Key",
            "api_key_prefix": "",
            "api_key_in": "header",
        }
    )
    with patch("urllib.request.build_opener") as mock_build_opener:
        mock_opener = MagicMock()
        mock_opener.open.return_value = mock_response
        mock_build_opener.return_value = mock_opener

        http_connector = RestConnector(config)
        http_connector.execute("GET", "http://example.com/api")

        req = mock_opener.open.call_args[0][0]
        assert req.get_header("X-api-key") == "mysecret"


def test_http_rest_api_key_query(mock_response):
    config = ConnectorConfig(
        params={
            "api_key": "mysecret",
            "api_key_in": "query",
            "api_key_query_param": "token",
        }
    )
    with patch("urllib.request.build_opener") as mock_build_opener:
        mock_opener = MagicMock()
        mock_opener.open.return_value = mock_response
        mock_build_opener.return_value = mock_opener

        http_connector = RestConnector(config)
        http_connector.execute("GET", "http://example.com/api")

        req = mock_opener.open.call_args[0][0]
        assert req.full_url == "http://example.com/api?token=mysecret"


@patch("urllib.request.HTTPBasicAuthHandler")
def test_http_rest_basic_auth(mock_basic_auth):
    config = ConnectorConfig(
        params={
            "auth_type": "basic",
            "username": "user",
            "password": "pwd",
            "base_url": "http://example.com",
        }
    )
    RestConnector(config)
    assert mock_basic_auth.called


@patch("urllib.request.HTTPCookieProcessor")
def test_http_rest_session(mock_cookie_processor):
    config = ConnectorConfig(params={"use_session": True})
    connector = RestConnector(config)
    assert mock_cookie_processor.called
    assert connector.cookie_jar is not None
