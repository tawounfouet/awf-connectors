import json

from pyconnectors.config import ConnectorConfig
from pyconnectors.factory import ConnectorFactory
import pyconnectors.connectors.http.rest  # noqa


def test_basic_auth_and_sessions():
    print("\n--- Basic Auth & Sessions ---")

    config = ConnectorConfig(
        params={
            "auth_type": "basic",
            "username": "user",
            "password": "password",
            "base_url": "https://httpbin.org",
            "use_session": True,
        }
    )
    http = ConnectorFactory.create("http.rest", config=config)

    # 1. Login with Basic Auth and get a cookie (httpbin returns auth status)
    result1 = http.safe_execute("GET", "https://httpbin.org/basic-auth/user/password")
    print("Auth Result Status:", "Success" if result1.success else "Failed")
    if result1.success:
        print("Data:", json.loads(result1.data["body"]))

    # 2. Set a cookie (to demonstrate session persistence)
    print("Setting a session cookie...")
    http.safe_execute("GET", "https://httpbin.org/cookies/set?mycookie=chocolate")

    # 3. Retrieve cookies
    result3 = http.safe_execute("GET", "https://httpbin.org/cookies")
    if result3.success:
        print("Cookies Retrieved:", json.loads(result3.data["body"]))


def test_api_key_header():
    print("\n--- API Key Auth (Header) ---")
    config = ConnectorConfig(
        params={
            "api_key": "super_secret_token",
            "api_key_header": "Authorization",
            "api_key_prefix": "Bearer",
        }
    )
    http = ConnectorFactory.create("http.rest", config=config)

    # Note: We inspect the headers received by httpbin
    result = http.safe_execute("GET", "https://httpbin.org/headers")
    if result.success:
        data = json.loads(result.data["body"])
        print("Sent Headers:", data.get("headers", {}).get("Authorization"))


def test_api_key_query():
    print("\n--- API Key Auth (Query Param) ---")
    config = ConnectorConfig(
        params={"api_key": "abc123xyz", "api_key_in": "query", "api_key_query_param": "token"}
    )
    http = ConnectorFactory.create("http.rest", config=config)

    result = http.safe_execute("GET", "https://httpbin.org/get")
    if result.success:
        data = json.loads(result.data["body"])
        print("Received Query Params:", data.get("args"))


def main():
    print("Running HTTP Authentication Examples using httpbin.org...")
    test_basic_auth_and_sessions()
    test_api_key_header()
    test_api_key_query()


if __name__ == "__main__":
    main()
