# Payment Connectors

Automate your payment processing and billing operations.

## Stripe (`payment.stripe`)

Provides a dynamic gateway to the official Stripe Python SDK.

**Requires:** `stripe` (Install with `pip install pyconnectors[payment]`)

### Configuration
- `api_key`: Your Stripe secret key (e.g., `sk_test_...`)

### Usage

The `execute` method maps directly to the Stripe SDK resources:
`execute(resource_name, action_name, **kwargs)`

```python
config = ConnectorConfig(params={"api_key": "sk_test_12345"})
stripe_conn = ConnectorFactory.create("payment.stripe", config=config)

# Creates a new customer
result = stripe_conn.execute("Customer", "create", email="test@example.com", name="John Doe")
print(result.id)

# Create a Checkout Session
session = stripe_conn.execute(
    "checkout.Session",
    "create",
    payment_method_types=['card'],
    mode='payment',
    success_url='https://example.com/success',
    cancel_url='https://example.com/cancel',
    line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {'name': 'T-shirt'},
            'unit_amount': 2000,
        },
        'quantity': 1,
    }]
)
```

## PayPal (`payment.paypal`)

Interacts with the PayPal REST API using OAuth2 automatically.

**Requires:** None (uses stdlib `urllib`)

### Configuration
- `client_id`: PayPal App Client ID
- `client_secret`: PayPal App Secret
- `environment`: `sandbox` (default) or `live`

### Usage

```python
config = ConnectorConfig(params={
    "client_id": "CLIENT_ID",
    "client_secret": "SECRET",
    "environment": "sandbox"
})
paypal = ConnectorFactory.create("payment.paypal", config=config)

# Example: Create an Order
payload = {
    "intent": "CAPTURE",
    "purchase_units": [{
        "amount": {
            "currency_code": "USD",
            "value": "100.00"
        }
    }]
}
result = paypal.execute("v2/checkout/orders", data=payload, method="POST")
print(result["data"]["id"])
```
