# Event Connectors

Manage ticketing, attendee tracking, and event operations through standard APIs.

## Eventbrite (`events.eventbrite`)

Connects to the Eventbrite v3 API easily using standard Python dependencies.

**Requires:** None (uses stdlib `urllib`)

### Configuration
- `private_token`: Your Eventbrite Personal OAuth token.

### Usage

```python
from pyconnectors.config import ConnectorConfig
from pyconnectors.factory import ConnectorFactory

config = ConnectorConfig(params={"private_token": "YOUR_PRIVATE_TOKEN"})
eventbrite = ConnectorFactory.create("events.eventbrite", config=config)

# Fetch current user's events
result = eventbrite.execute("users/me/events", data={"status": "live"}, method="GET")

if result["status"] == 200:
    for event in result["data"].get("events", []):
        print(f"Event: {event['name']['text']}")
else:
    print("Failed:", result["error"])
```
