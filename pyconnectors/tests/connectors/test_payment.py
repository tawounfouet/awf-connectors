import json
import pytest
from unittest.mock import MagicMock, patch

from pyconnectors.config import ConnectorConfig
from pyconnectors.connectors.payment.helloasso import HelloAssoConnector
from pyconnectors.connectors.payment.paypal import PayPalConnector
from pyconnectors.connectors.payment.stripe_api import StripeConnector


@patch("pyconnectors.connectors.payment.stripe_api.stripe")
def test_stripe_connector_execute(mock_stripe):
    if mock_stripe is None:
        pytest.skip("stripe not available")

    config = ConnectorConfig(params={"api_key": "sk_test_123"})
    connector = StripeConnector(config)

    mock_customer = MagicMock()
    mock_stripe.Customer = mock_customer
    mock_customer.create.return_value = {"id": "cus_123", "email": "test@test.com"}

    result = connector.execute("Customer", "create", email="test@test.com")

    assert result == {"id": "cus_123", "email": "test@test.com"}
    assert mock_stripe.api_key == "sk_test_123"
    mock_customer.create.assert_called_with(email="test@test.com")


@patch("urllib.request.urlopen")
def test_paypal_connector_execute(mock_urlopen):
    config = ConnectorConfig(
        params={
            "client_id": "client123",
            "client_secret": "secret123",
            "environment": "sandbox",
        }
    )
    connector = PayPalConnector(config)

    # We need to mock two consecutive HTTP calls:
    # 1. Fetching the token
    # 2. Making the actual request

    token_response = MagicMock()
    token_response.read.return_value = b'{"access_token": "mock_paypal_token"}'
    token_context = MagicMock()
    token_context.__enter__.return_value = token_response

    api_response = MagicMock()
    api_response.status = 201
    api_response.read.return_value = b'{"id": "PAYID-123"}'
    api_context = MagicMock()
    api_context.__enter__.return_value = api_response

    mock_urlopen.side_effect = [token_context, api_context]

    result = connector.execute("v2/checkout/orders", data={"intent": "CAPTURE"}, method="POST")

    assert result["status"] == 201
    assert result["data"]["id"] == "PAYID-123"

    # Verify token call
    token_call_args = mock_urlopen.call_args_list[0][0][0]
    assert token_call_args.full_url == "https://api-m.sandbox.paypal.com/v1/oauth2/token"
    assert token_call_args.get_method() == "POST"
    assert token_call_args.get_header("Authorization").startswith("Basic ")

    # Verify API call
    api_call_args = mock_urlopen.call_args_list[1][0][0]
    assert api_call_args.full_url == "https://api-m.sandbox.paypal.com/v2/checkout/orders"
    assert api_call_args.get_method() == "POST"
    assert api_call_args.get_header("Authorization") == "Bearer mock_paypal_token"
    assert api_call_args.get_header("Content-type") == "application/json"

    payload = json.loads(api_call_args.data.decode("utf-8"))
    assert payload["intent"] == "CAPTURE"


@patch("urllib.request.urlopen")
def test_helloasso_connector_execute(mock_urlopen):
    config = ConnectorConfig(params={"client_id": "client_ha", "client_secret": "secret_ha"})
    connector = HelloAssoConnector(config)

    # 1. Mock the token endpoint response
    token_response = MagicMock()
    token_response.read.return_value = b'{"access_token": "mock_helloasso_token"}'
    token_context = MagicMock()
    token_context.__enter__.return_value = token_response

    # 2. Mock the actual API response
    api_response = MagicMock()
    api_response.status = 200
    api_response.read.return_value = b'{"data": [{"id": "camp1"}]}'
    api_context = MagicMock()
    api_context.__enter__.return_value = api_response

    mock_urlopen.side_effect = [token_context, api_context]

    result = connector.execute("organizations/my-org/campaigns", method="GET")

    assert result["status"] == 200
    assert result["data"]["data"][0]["id"] == "camp1"

    # Verify token call
    token_call_args = mock_urlopen.call_args_list[0][0][0]
    assert token_call_args.full_url == "https://api.helloasso.com/v5/oauth2/token"
    assert token_call_args.get_method() == "POST"

    token_payload = urllib.parse.parse_qs(token_call_args.data.decode("utf-8"))
    assert token_payload["client_id"][0] == "client_ha"
    assert token_payload["grant_type"][0] == "client_credentials"

    # Verify API call
    api_call_args = mock_urlopen.call_args_list[1][0][0]
    assert api_call_args.full_url == "https://api.helloasso.com/v5/organizations/my-org/campaigns"
    assert api_call_args.get_method() == "GET"
    assert api_call_args.get_header("Authorization") == "Bearer mock_helloasso_token"
