from pyconnectors.config import ConnectorConfig
from pyconnectors.factory import ConnectorFactory
import pyconnectors.connectors.http.rest  # noqa - ensure registration


def main():
    config = ConnectorConfig()

    # Using Factory
    http = ConnectorFactory.create("http.rest", config=config)

    print("Fetching data...")
    result = http.safe_execute("GET", "https://jsonplaceholder.typicode.com/todos/1")

    if result.success:
        print(f"Success! Duration: {result.duration:.2f}s")
        print("Data:", result.data["body"])
    else:
        print("Failed:", result.error)


if __name__ == "__main__":
    main()
