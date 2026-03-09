import pytest
from pyconnectors.registry import ConnectorRegistry


@pytest.fixture(autouse=True)
def clean_registry():
    """Clear the registry before and after each test to ensure isolation."""
    ConnectorRegistry.clear()
    yield
    ConnectorRegistry.clear()
