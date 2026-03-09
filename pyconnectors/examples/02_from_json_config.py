import json
import tempfile
from pyconnectors.config import ConnectorConfig
from pyconnectors.factory import ConnectorFactory
import pyconnectors.connectors.http.rest  # noqa


def main():
    # Create a temporary JSON config file
    config_data = {"timeout": 10, "retries": 3, "base_url": "https://api.example.com"}

    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
        json.dump(config_data, f)
        config_path = f.name

    print(f"Loading config from {config_path}")

    # Load configuration
    config = ConnectorConfig.from_json_file(config_path)

    # Create connector
    connector = ConnectorFactory.create("http.rest", config=config)
    print("Connector initialized with params:", connector.config.params)


if __name__ == "__main__":
    main()
