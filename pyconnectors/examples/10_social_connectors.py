import os
from pyconnectors.config import ConnectorConfig
from pyconnectors.factory import ConnectorFactory

import pyconnectors.connectors.social.twitter  # noqa


def main():
    print("Social Connectors Example - Twitter (X) API v2")

    # The Twitter connector uses a Bearer Token for authentication.
    # It requires no external dependencies.
    config = ConnectorConfig(
        params={"bearer_token": os.environ.get("TWITTER_BEARER_TOKEN", "mock_token")}
    )

    twitter = ConnectorFactory.create("social.twitter", config=config)

    # Use safe_execute to avoid crashing on fake tokens
    result = twitter.safe_execute("users/me")

    if result.success:
        print("Twitter API Call Success!")
        print("Data:", result.data)
    else:
        print("Twitter API Call Failed (Expected if mock_token is used).")
        print("Error:", result.error)


if __name__ == "__main__":
    main()
