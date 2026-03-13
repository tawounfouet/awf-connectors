# Social Connectors

Social connectors interact with major social network APIs using 0-dependency native requests via `urllib.request`.

## Social Platforms

### Facebook Graph API (`social.facebook`)
- **Requires:** Nothing (uses stdlib)
- **Config:** `access_token`, `api_version` (default: `v19.0`)
- **Usage:**
  ```python
  fb = ConnectorFactory.create("social.facebook", config)
  fb.execute("me")
  ```

### LinkedIn REST API (`social.linkedin`)
- **Requires:** Nothing (uses stdlib)
- **Config:** `access_token`
- **Usage:**
  ```python
  li = ConnectorFactory.create("social.linkedin", config)
  li.execute("me")
  ```

### Twitter / X v2 API (`social.twitter`)
- **Requires:** Nothing (uses stdlib)
- **Config:** `bearer_token`
- **Usage:**
  ```python
  tw = ConnectorFactory.create("social.twitter", config)
  tw.execute("users/me")
  ```

### TikTok Display API (`social.tiktok`)
- **Requires:** Nothing (uses stdlib)
- **Config:** `access_token`
- **Usage:**
  ```python
  tk = ConnectorFactory.create("social.tiktok", config)
  tk.execute("user/info/")
  ```

### Instagram Graph API (`social.instagram`)
- **Requires:** Nothing (uses stdlib)
- **Config:** `access_token`, `api_version` (default: `v19.0`)
- **Usage:**
  ```python
  ig = ConnectorFactory.create("social.instagram", config)
  ig.execute("me/media")
  ```

### Discord Webhooks (`social.discord`)
- **Requires:** Nothing (uses stdlib)
- **Config:** `webhook_url`
- **Usage:**
  ```python
  discord = ConnectorFactory.create("social.discord", config)
  discord.execute("Hello from PyConnectors!", username="Bot")
  ```

### Microsoft Teams Webhooks (`social.teams`)
- **Requires:** Nothing (uses stdlib)
- **Config:** `webhook_url`
- **Usage:**
  ```python
  teams = ConnectorFactory.create("social.teams", config)
  teams.execute("Pipeline failed.", title="Alert", theme_color="FF0000")
  ```

### Slack Webhooks (`social.slack`)
- **Requires:** Nothing (uses stdlib)
- **Config:** `webhook_url`
- **Usage:**
  ```python
  slack = ConnectorFactory.create("social.slack", config)
  slack.execute("Hello from PyConnectors!", channel="#general")
  ```

### WhatsApp Cloud API (`social.whatsapp`)
- **Requires:** Nothing (uses stdlib)
- **Config:** `access_token`, `phone_number_id` (can also be passed in `execute()`), `api_version` (default: `v19.0`)
- **Usage:**
  ```python
  wa = ConnectorFactory.create("social.whatsapp", config)
  wa.execute("15551234567", "Hello World!")
  ```
