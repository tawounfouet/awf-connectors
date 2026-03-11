import os
from pyconnectors.config import ConnectorConfig
from pyconnectors.factory import ConnectorFactory

import pyconnectors.connectors.auth.jwt_auth  # noqa
import pyconnectors.connectors.auth.oauth2  # noqa
import pyconnectors.connectors.http.oauth2  # noqa


def test_jwt():
    print("\n--- JWT Authentication ---")

    # Needs pip install pyconnectors[auth]
    try:
        import jwt
    except ImportError:
        print("Skipping JWT Example: PyJWT not installed.")
        return

    config = ConnectorConfig(params={"secret_key": "super_secret_key"})
    jwt_conn = ConnectorFactory.create("auth.jwt", config=config)

    # 1. Encode
    payload = {"user_id": 42, "role": "admin"}
    print(f"Original Payload: {payload}")

    result_enc = jwt_conn.safe_execute("encode", payload=payload)
    if not result_enc.success:
        print("Encoding failed:", result_enc.error)
        return

    token = result_enc.data["token"]
    print(f"Encoded Token: {token}")

    # 2. Decode
    result_dec = jwt_conn.safe_execute("decode", token=token)
    print("Decoded Payload:", result_dec.data["payload"])


def test_oauth2_wrapper():
    print("\n--- HTTP OAuth2 REST Wrapper ---")

    # This automatically fetches a token from auth server, then queries the API
    config = ConnectorConfig(
        params={
            "oauth2_token_url": "https://httpbin.org/post",  # mock token endpoint
            "oauth2_client_id": "client_123",
            "oauth2_client_secret": "secret_abc",
        }
    )

    # Initialize the wrapper connector
    api = ConnectorFactory.create("http.oauth2", config=config)

    # We use safe_execute. It will try to fetch a token from httpbin (which will return JSON containing the token request)
    # Since httpbin doesn't actually return a valid OAuth2 "access_token" format, it will fail gracefully here,
    # but demonstrates the execution flow natively.
    print("Executing request with auto-token injection...")
    result = api.safe_execute("GET", "https://httpbin.org/bearer")

    if result.success:
        print("Success:", result.data)
    else:
        print("Expected Failure (httpbin doesn't return real OAuth2 tokens):", result.error)


def main():
    print("Running Authentication Connectors Examples...")
    test_jwt()
    test_oauth2_wrapper()


if __name__ == "__main__":
    main()
