# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial core architecture (0-dependency).
- Framework components: BaseConnector, ConnectorConfig, ConnectorFactory, ConnectorRegistry, ConnectorResult, exceptions.
- Hooks for pre_execute, post_execute, on_error.
- Connectors: HTTP (REST), Database (PostgreSQL), Email (SMTP), Messaging (placeholder), Storage (S3), Social (Slack).
- Typer/Rich CLI interface (`list`, `inspect`, `run`, `test`).
- Contrib modules for Django and FastAPI.
- Unit testing with pytest and mocking.
- Source distribution layout (`src/pyconnectors`).
- Complete `pyproject.toml` with Ruff, Black, Mypy, and Pytest configuration.
