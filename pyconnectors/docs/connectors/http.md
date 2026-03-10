# HTTP Connectors

The HTTP connectors provide standard ways to interact with REST APIs and Webhooks natively without external libraries.

## `http.rest`

**Requires:** None (uses stdlib `urllib`)

### Configuration

The `RestConnector` relies on parameters passed directly into `execute()` rather than `ConnectorConfig` for simplicity, but you can set headers globally.

### Usage

```python
from pyconnectors.config import ConnectorConfig
from pyconnectors.factory import ConnectorFactory

config = ConnectorConfig()
http = ConnectorFactory.create("http.rest", config=config)

result = http.execute("GET", "https://api.github.com/users/octocat")
print(result["status"])
print(result["body"])
```
