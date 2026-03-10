# Email Connectors

PyConnectors supports sending and reading emails via standard protocols, convenient webmail wrappers, and modern transactional APIs.

## Protocols
- `email.smtp`: Send emails securely. Requires `host`, `port`, `user`, `password`, `from_addr`.
- `email.imap`: Search and read emails. Requires `host`, `port`, `user`, `password`, `use_ssl`.
- `email.pop3`: Fetch basic inbox stats. Requires `host`, `port`, `user`, `password`, `use_ssl`.

## Webmail Wrappers
Pre-configured wrappers using `smtplib` for ease of use:
- `email.gmail` (Uses `smtp.gmail.com:587`)
- `email.outlook` (Uses `smtp-mail.outlook.com:587`)
- `email.yahoo` (Uses `smtp.mail.yahoo.com:465` with SSL)

*Note: You must generate App Passwords for these services if 2FA is enabled.*

### Usage
```python
config = ConnectorConfig(params={"user": "me@gmail.com", "password": "app_password"})
gmail = ConnectorFactory.create("email.gmail", config=config)

gmail.execute("to@example.com", "Hello!", "This is the body.")
```

## Transactional APIs
Send emails without relying on SMTP by using modern HTTP-based REST APIs.
All of these use the `urllib` standard library and do not require external HTTP clients.

- `email.resend` (Requires `api_key`, `from_addr`)
- `email.brevo` (Requires `api_key`, `from_addr`)
- `email.mailchimp` (Requires `api_key`, `from_addr`)
- `email.mailersend` (Requires `api_key`, `from_addr`)
- `email.mailgun` (Requires `api_key`, `domain`, `from_addr`)

### Usage
```python
config = ConnectorConfig(params={"api_key": "re_123...", "from_addr": "info@my-domain.com"})
resend = ConnectorFactory.create("email.resend", config=config)

resend.execute("to@example.com", "Hello!", "<p>This is the HTML body.</p>")
```

## Amazon SES
- `email.ses`
**Requires:** `boto3` (Install with `pip install pyconnectors[s3]`)

### Configuration
- `aws_access_key_id`
- `aws_secret_access_key`
- `region_name` (default `us-east-1`)
- `from_addr`

### Usage
```python
ses = ConnectorFactory.create("email.ses", config=config)
ses.execute("to@example.com", "Subject", "<p>HTML</p>", body_text="Plain text fallback")
```
