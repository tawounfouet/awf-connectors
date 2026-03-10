# PyConnectors Quickstart

## 1. Installation

Install the base package:
```bash
pip install pyconnectors
```

Install with specific connector dependencies:
```bash
pip install pyconnectors[postgresql,s3,cli]
```

## 2. Basic Usage

```python
from pyconnectors.config import ConnectorConfig
from pyconnectors.factory import ConnectorFactory

# 1. Define configuration
config = ConnectorConfig(params={"base_url": "https://api.github.com"})

# 2. Instantiate via Factory
http = ConnectorFactory.create("http.rest", config=config)

# 3. Execute safely
result = http.safe_execute("GET", "https://api.github.com/users/octocat")

if result.success:
    print(result.data)
else:
    print("Error:", result.error)
```

## 3. Loading Configuration

### From JSON:
```python
config = ConnectorConfig.from_json_file("config.json")
```

### From Environment Variables:
```python
# Assuming ENV vars like PYCONN_API_KEY="secret"
config = ConnectorConfig.from_env("PYCONN_")
```

## 4. Using the CLI

If installed with `[cli]`:
```bash
# List all available connectors
pyconnectors list

# Inspect a specific connector
pyconnectors inspect database.postgresql

# Run a connector from a JSON config file
pyconnectors run config.json
```
