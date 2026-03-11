# Fitness Connectors

Connect to health and fitness APIs.

## Strava (`fitness.strava`)

Connect to the Strava v3 API to fetch athlete and activity data.

**Requires:** None (uses stdlib `urllib`)

### Configuration
- `access_token`: The OAuth2 Access Token for the user.

### Usage

```python
from pyconnectors.config import ConnectorConfig
from pyconnectors.factory import ConnectorFactory

config = ConnectorConfig(params={"access_token": "your_strava_token"})
strava = ConnectorFactory.create("fitness.strava", config=config)

# Fetch current athlete's activities
result = strava.execute("athlete/activities", data={"per_page": 5}, method="GET")

if result["status"] == 200:
    for activity in result["data"]:
        print(f"Activity: {activity['name']} - Distance: {activity['distance']}m")
```
