# Authentication Connectors

The `auth` connectors handle token generation, OAuth2 flows, and SSO strategies (SAML / OIDC).
You can install external dependencies needed with:
```bash
pip install pyconnectors[auth]
```

## JWT (`auth.jwt`)
**Requires:** `PyJWT`

Generate and validate JSON Web Tokens securely.

```python
config = ConnectorConfig(params={"secret_key": "my_secret", "algorithm": "HS256"})
jwt_conn = ConnectorFactory.create("auth.jwt", config=config)

# Encode
token = jwt_conn.execute("encode", payload={"user_id": 123})["token"]

# Decode
payload = jwt_conn.execute("decode", token=token)["payload"]
```

## OAuth2 (`auth.oauth2`)
**Requires:** None (uses stdlib `urllib`)

Handles basic token exchanges.

```python
config = ConnectorConfig(params={
    "token_url": "https://auth.server.com/token",
    "client_id": "client_abc",
    "client_secret": "secret_xyz"
})
oauth2 = ConnectorFactory.create("auth.oauth2", config=config)

# Fetch client credentials
result = oauth2.execute("client_credentials")

# Refresh a token
result = oauth2.execute("refresh_token", refresh_token="old_refresh_token")
```

## OAuth2 REST Wrapper (`http.oauth2`)
**Requires:** None

Automatically fetches and injects OAuth2 Bearer tokens into API requests. It extends the `http.rest` connector.

```python
config = ConnectorConfig(params={
    "oauth2_token_url": "https://auth.server.com/token",
    "oauth2_client_id": "client_abc",
    "oauth2_client_secret": "secret_xyz"
})
api = ConnectorFactory.create("http.oauth2", config=config)

# Will automatically fetch token and append Authorization header
api.execute("GET", "https://api.server.com/protected_resource")
```

## OpenID Connect (`auth.oidc`)
**Requires:** None

Generates authorization URLs and handles code-to-token exchanges.

```python
config = ConnectorConfig(params={
    "issuer": "https://idp.example.com",
    "client_id": "client_id",
    "client_secret": "client_secret"
})
oidc = ConnectorFactory.create("auth.oidc", config=config)

# Generate login URL
url = oidc.execute("auth_url", redirect_uri="https://myapp.com/callback")

# Exchange authorization code for token
token = oidc.execute("exchange_code", auth_code="code_123", redirect_uri="https://myapp.com/callback")
```

## SAML 2.0 (`auth.saml`)
**Requires:** `python3-saml`

Perform robust SAML 2.0 authentications (acts as an SP).

```python
config = ConnectorConfig(params={
    "saml_settings": {
        "strict": True,
        "sp": { ... },
        "idp": { ... }
    }
})
saml = ConnectorFactory.create("auth.saml", config=config)

# Process IdP response payload
result = saml.execute(request_data, action="process_response")
print(result["attributes"])
```
