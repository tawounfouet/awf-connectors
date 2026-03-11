import pytest
from unittest.mock import MagicMock, patch

from pyconnectors.config import ConnectorConfig
from pyconnectors.connectors.auth.jwt_auth import JWTConnector
from pyconnectors.connectors.auth.oauth2 import OAuth2Connector
from pyconnectors.connectors.auth.saml import SAMLConnector
from pyconnectors.connectors.auth.oidc import OIDCConnector
from pyconnectors.connectors.http.oauth2 import OAuth2RestConnector


@patch("pyconnectors.connectors.auth.jwt_auth.jwt")
def test_jwt_connector_encode(mock_jwt):
    if mock_jwt is None:
        pytest.skip("PyJWT not available")

    config = ConnectorConfig(params={"secret_key": "supersecret"})
    connector = JWTConnector(config)

    mock_jwt.encode.return_value = "header.payload.signature"

    result = connector.execute("encode", payload={"user_id": 123})

    assert result["status"] == "success"
    assert result["token"] == "header.payload.signature"
    mock_jwt.encode.assert_called_with({"user_id": 123}, "supersecret", algorithm="HS256")


@patch("pyconnectors.connectors.auth.jwt_auth.jwt")
def test_jwt_connector_decode(mock_jwt):
    if mock_jwt is None:
        pytest.skip("PyJWT not available")

    config = ConnectorConfig(params={"secret_key": "supersecret"})
    connector = JWTConnector(config)

    mock_jwt.decode.return_value = {"user_id": 123}

    result = connector.execute("decode", token="header.payload.signature")

    assert result["status"] == "success"
    assert result["payload"] == {"user_id": 123}
    mock_jwt.decode.assert_called_with(
        "header.payload.signature", "supersecret", algorithms=["HS256"]
    )


@patch("urllib.request.urlopen")
def test_oauth2_connector_client_credentials(mock_urlopen):
    config = ConnectorConfig(
        params={
            "token_url": "https://auth.example.com/token",
            "client_id": "my_client",
            "client_secret": "my_secret",
            "scopes": ["read", "write"],
        }
    )
    connector = OAuth2Connector(config)

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value = b'{"access_token": "abc123token"}'
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_context

    result = connector.execute("client_credentials")

    assert result["status"] == "success"
    assert result["data"]["access_token"] == "abc123token"

    req = mock_urlopen.call_args[0][0]
    assert req.full_url == "https://auth.example.com/token"
    assert b"grant_type=client_credentials" in req.data
    assert b"client_id=my_client" in req.data


@patch("pyconnectors.connectors.auth.saml.OneLogin_Saml2_Auth")
def test_saml_connector_login_url(mock_saml_auth_class):
    if mock_saml_auth_class is None:
        pytest.skip("python3-saml not available")

    config = ConnectorConfig(params={"saml_settings": {"idp": {"entityId": "..."}}})
    connector = SAMLConnector(config)

    mock_auth_instance = MagicMock()
    mock_saml_auth_class.return_value = mock_auth_instance
    mock_auth_instance.login.return_value = "https://idp.example.com/login"

    request_data = {"https": "on", "http_host": "sp.example.com", "script_name": "/acs"}
    result = connector.execute(request_data, action="login_url")

    assert result["status"] == "success"
    assert result["url"] == "https://idp.example.com/login"


def test_oidc_connector_auth_url():
    config = ConnectorConfig(
        params={
            "issuer": "https://idp.example.com",
            "client_id": "client123",
            "client_secret": "secret",
        }
    )
    connector = OIDCConnector(config)
    result = connector.execute("auth_url", redirect_uri="https://app.com/callback")

    assert result["status"] == "success"
    assert "https://idp.example.com/protocol/openid-connect/auth" in result["url"]
    assert "client_id=client123" in result["url"]
    assert "redirect_uri=https%3A%2F%2Fapp.com%2Fcallback" in result["url"]


@patch("urllib.request.urlopen")
def test_http_oauth2_rest_connector(mock_urlopen):
    # This connector relies on OAuth2Connector internally.
    config = ConnectorConfig(
        params={
            "oauth2_token_url": "https://auth.com/token",
            "oauth2_client_id": "my_client",
            "oauth2_client_secret": "my_secret",
        }
    )
    connector = OAuth2RestConnector(config)

    # We will mock the auth_connector internally to avoid two network calls
    connector.auth_connector = MagicMock()

    auth_result = MagicMock()
    auth_result.success = True
    auth_result.data = {"data": {"access_token": "injected_token_123"}}
    connector.auth_connector.safe_execute.return_value = auth_result

    # Mock the actual HTTP API call
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value = b'{"success": true}'
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_response

    # We patch build_opener inside RestConnector so we control the opener's output
    with patch("urllib.request.build_opener") as mock_build_opener:
        mock_opener = MagicMock()
        mock_opener.open.return_value = mock_context
        mock_build_opener.return_value = mock_opener

        # We need to force re-initialization of opener with the patch active
        connector._build_opener()

        result = connector.execute("GET", "https://api.com/data")

        assert result["status"] == 200
        assert connector.auth_connector.safe_execute.called

        # Verify the Auth header was injected
        req = mock_opener.open.call_args[0][0]
        assert req.get_header("Authorization") == "Bearer injected_token_123"
