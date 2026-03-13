# CRM Connectors

Manage customers, leads, and tracking funnels efficiently.

## HubSpot (`crm.hubspot`)

Interact with the HubSpot API to manage contacts, companies, and deals.

**Requires:** None (uses stdlib `urllib`)

### Configuration
- `access_token`: The HubSpot App Private App Access Token or OAuth2 token.

### Usage

```python
from pyconnectors.config import ConnectorConfig
from pyconnectors.factory import ConnectorFactory

config = ConnectorConfig(params={"access_token": "pat-eu1-..."})
hubspot = ConnectorFactory.create("crm.hubspot", config=config)

# Fetch latest 10 contacts
result = hubspot.execute("crm/v3/objects/contacts", data={"limit": 10}, method="GET")

if result["status"] == 200:
    for contact in result["data"].get("results", []):
        print(f"Contact ID: {contact['id']}")

# Create a new contact
new_contact_payload = {
    "properties": {
        "email": "new.user@example.com",
        "firstname": "John",
        "lastname": "Doe"
    }
}
create_res = hubspot.execute("crm/v3/objects/contacts", data=new_contact_payload, method="POST")
print("New Contact ID:", create_res["data"]["id"])
```
