import os
from pyconnectors.config import ConnectorConfig
from pyconnectors.factory import ConnectorFactory
import pyconnectors.connectors.database.postgresql  # noqa


def main():
    # Set mock environment variables
    os.environ["PG_DSN"] = "postgres://user:pass@localhost:5432/db"
    os.environ["PG_POOL_SIZE"] = "10"

    print("Loading config from ENV using prefix 'PG_'")
    config = ConnectorConfig.from_env("PG_")

    # Creates PostgreSQL Connector
    # Using 'database.postgresql' connector
    connector = ConnectorFactory.create("database.postgresql", config=config)

    print(f"Connector Params: {connector.config.params}")

    # Clean up mock environment variables
    del os.environ["PG_DSN"]
    del os.environ["PG_POOL_SIZE"]


if __name__ == "__main__":
    main()
