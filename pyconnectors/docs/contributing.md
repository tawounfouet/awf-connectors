# Contributing to PyConnectors

We love your input! We want to make contributing to this project as easy and transparent as possible.

## Development Setup

1. Fork the repo and create your branch from `main`.
2. Install the project in editable mode with development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run `make check` to ensure your environment is set up correctly (this runs formatting, linting, and tests).

## Adding a New Connector

1. Choose the appropriate directory under `src/pyconnectors/connectors/`. If you are adding a completely new category, create a new directory and an `__init__.py`.
2. Create your connector class inheriting from `BaseConnector`.
3. Use the `@connector("category.name")` decorator to register it.
4. Implement the `execute()` method.
5. If your connector requires an external library, wrap the import in a `try/except ImportError` block. Raise an informative `ImportError` inside `execute()` if the library is missing.
6. Add the dependency to the `[project.optional-dependencies]` section in `pyproject.toml` (e.g., `my_connector = ["my_lib"]`).
7. Write tests using `pytest` and `unittest.mock` under `tests/connectors/`.
8. Register your connector by adding an import statement in `src/pyconnectors/cli/commands/list.py`.

## Code Quality

All code must pass:
- **Black**: `make format`
- **Ruff**: `make lint`
- **Mypy**: `make lint` (strict typing is enforced)
- **Pytest**: `make test`

Run `make check` before submitting a Pull Request.
