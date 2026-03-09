# PyConnectors

**A universal framework for external service connectors.**

PyConnectors is a lightweight, modular, type-safe, and extensible Python library designed to standardize connections to external services (APIs, databases, messaging queues, object storage, etc.).

## Features
- **Ultra-light Core**: The core library has 0 external dependencies.
- **Strict Typing**: Fully typed with `dataclasses` and `typing`, compatible with `mypy`.
- **Hooks & Middleware**: Run logic before execution, after execution, or on error.
- **Standardized Results**: Every connector returns a uniform `ConnectorResult`.
- **Extensible**: Easily build your own connectors using `@connector`.
- **CLI Included**: Test and run connectors directly from your terminal.

## Installation

Install the core library:

```bash
pip install pyconnectors
```

Or install with specific connectors:

```bash
pip install pyconnectors[postgresql]
pip install pyconnectors[s3]
pip install pyconnectors[cli]
```

## Quick Start

```python
from pyconnectors.config import ConnectorConfig
from pyconnectors.factory import ConnectorFactory

# Configuration is decoupled from logic
config = ConnectorConfig(params={"base_url": "https://api.github.com"})

# Instantiate the connector
http = ConnectorFactory.create("http.rest", config=config)

# Execute safely, capturing exceptions and execution time
result = http.safe_execute("GET", "https://api.github.com/users/octocat")

if result.success:
    print(f"Data retrieved in {result.duration:.2f} seconds!")
    print(result.data)
else:
    print(f"Execution failed: {result.error}")
```

## Creating Custom Connectors

```python
from pyconnectors.base import BaseConnector
from pyconnectors.registry import connector

@connector("my.custom.service")
class CustomConnector(BaseConnector):
    def execute(self, endpoint: str):
        api_key = self.config.params.get("api_key")
        # Custom logic goes here
        return {"status": "ok", "endpoint": endpoint}
```

## CLI Usage

List available connectors:
```bash
pyconnectors list
```

Inspect a connector:
```bash
pyconnectors inspect http.rest
```

## License

MIT License
