from pyconnectors.config import ConnectorConfig
from pyconnectors.factory import ConnectorFactory

import pyconnectors.connectors.database.sqlite  # noqa


def main():
    print("Testing SQLite Connector (Standard Library)")

    # Use an in-memory database
    config = ConnectorConfig(params={"database": ":memory:"})
    sqlite = ConnectorFactory.create("database.sqlite", config=config)

    # 1. Create table
    sqlite.safe_execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)

    # 2. Insert data
    sqlite.safe_execute(
        "INSERT INTO users (name, email) VALUES (?, ?)", ("Alice", "alice@example.com")
    )
    sqlite.safe_execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Bob", "bob@example.com"))

    # 3. Query data
    result = sqlite.safe_execute("SELECT * FROM users")

    if result.success:
        print("\nUsers found:")
        for row in result.data:
            print(f"- {row['name']} ({row['email']})")
    else:
        print("Error querying database:", result.error)


if __name__ == "__main__":
    main()
