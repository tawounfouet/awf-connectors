# PyConnectors Architecture

The `pyconnectors` library is built around a lightweight, zero-dependency core that standardizes how Python applications interact with external services.

## Core Concepts

### 1. The Registry Pattern (`ConnectorRegistry`)
All connectors are registered centrally using the `@connector("namespace.name")` decorator. This allows dynamic lookup and instantiation via string names without needing to import specific classes manually.

### 2. Configuration (`ConnectorConfig`)
A `dataclass` representing configuration. It natively supports loading parameters from dictionaries, JSON files, or Environment Variables (via prefixes).

### 3. The Factory (`ConnectorFactory`)
A utility class responsible for looking up a connector in the registry and injecting the `ConnectorConfig` during instantiation.

### 4. Base Abstraction (`BaseConnector`)
Every connector extends `BaseConnector`. It mandates the implementation of an `execute()` method.
It also provides a `safe_execute()` method that wraps `execute()` to:
- Capture timing metrics (duration).
- Provide unified error handling.
- Trigger lifecycle hooks (`pre_execute`, `post_execute`, `on_error`).
- Return a standard `ConnectorResult`.

### 5. Standardized Output (`ConnectorResult`)
A standard `dataclass` returned by `safe_execute()` ensuring every connector response is uniform:
- `success`: Boolean indicating if the execution was successful.
- `data`: The raw output from the connector.
- `error`: Error message if `success` is False.
- `duration`: Execution time in seconds.
- `metadata`: Any additional context.

## Modularity & Dependencies
The core (`pyconnectors.base`, `pyconnectors.config`, etc.) has **0 external dependencies**, relying entirely on the Python standard library. External libraries (like `psycopg`, `boto3`, `pymongo`) are only imported when a specific connector is invoked. If the required library is missing, a clear `ImportError` is raised indicating which `extras` package to install.
