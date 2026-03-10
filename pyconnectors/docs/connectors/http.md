# HTTP Connectors

The HTTP connectors provide standard ways to interact with REST APIs and Webhooks natively without external libraries.

## `http.rest`

**Requires:** None (uses stdlib `urllib`)

### Configuration
The `RestConnector` supports advanced configuration via `ConnectorConfig` for robust authentication.

**Authentication Parameters:**
- **API Key (Header):**
  - `api_key`: The token string.
  - `api_key_in`: `"header"` (default).
  - `api_key_header`: The header name (default `"Authorization"`).
  - `api_key_prefix`: The prefix (default `"Bearer"`, set to `""` to remove).
- **API Key (Query Parameter):**
  - `api_key`: The token string.
  - `api_key_in`: `"query"`.
  - `api_key_query_param`: The parameter name (default `"api_key"`).
- **Basic & Digest Auth:**
  - `auth_type`: `"basic"` or `"digest"`.
  - `username` and `password`.
  - `base_url`: Used to map the authentication realm.
- **Sessions:**
  - `use_session`: `True` to persist cookies automatically across requests in the same instance.

### Usage Examples

**Basic GET Request:**
```python
from pyconnectors.config import ConnectorConfig
from pyconnectors.factory import ConnectorFactory

config = ConnectorConfig()
http = ConnectorFactory.create("http.rest", config=config)

result = http.execute("GET", "https://api.github.com/users/octocat")
```

**Bearer Token Auth:**
```python
config = ConnectorConfig(
    params={
        "api_key": "my_secret_token",
        "api_key_header": "Authorization",
        "api_key_prefix": "Bearer"
    }
)
http = ConnectorFactory.create("http.rest", config=config)
http.execute("GET", "https://api.example.com/protected")
```

**Basic Authentication & Persistent Sessions:**
```python
config = ConnectorConfig(
    params={
        "auth_type": "basic",
        "username": "admin",
        "password": "password123",
        "base_url": "https://httpbin.org",
        "use_session": True
    }
)
http = ConnectorFactory.create("http.rest", config=config)

# Logs in and captures cookies
http.execute("GET", "https://httpbin.org/basic-auth/admin/password123")

# Next request automatically uses the captured session cookie
http.execute("GET", "https://httpbin.org/cookies")
```
