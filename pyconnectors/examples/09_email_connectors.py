import os
from pyconnectors.config import ConnectorConfig
from pyconnectors.factory import ConnectorFactory

# Import all needed connectors
import pyconnectors.connectors.email.resend  # noqa
import pyconnectors.connectors.email.gmail  # noqa


def main():
    print("Email Connectors Example\n")

    # --- 1. Using a Transactional API (Resend) ---
    resend_api_key = os.environ.get("RESEND_API_KEY", "re_123456789")
    resend_config = ConnectorConfig(
        params={"api_key": resend_api_key, "from_addr": "onboarding@resend.dev"}
    )

    # Since this is an example, we might not have a real API key.
    # We will use safe_execute to catch the expected authentication error.
    print("Attempting to send via Resend API...")
    resend = ConnectorFactory.create("email.resend", config=resend_config)

    resend_result = resend.safe_execute(
        to_addr="test@example.com",
        subject="Welcome to PyConnectors!",
        body_html="<h1>Hello!</h1><p>This was sent using the Resend connector.</p>",
    )

    if resend_result.success:
        print("Success!", resend_result.data)
    else:
        print("Expected failure (invalid API key):", resend_result.error)

    print("\n-------------------------------\n")

    # --- 2. Using a Webmail Wrapper (Gmail) ---
    gmail_config = ConnectorConfig(
        params={
            "user": "your_email@gmail.com",
            "password": "your_app_password",  # Requires an App Password
        }
    )

    # We won't execute this one as it would definitely fail without valid credentials,
    # but this shows how it's instantiated.
    ConnectorFactory.create("email.gmail", config=gmail_config)
    print("Gmail connector instantiated successfully. Ready to send emails via SMTP.")


if __name__ == "__main__":
    main()
