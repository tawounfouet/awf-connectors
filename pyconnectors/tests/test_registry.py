import pytest
from typing import Any
from pyconnectors.base import BaseConnector
from pyconnectors.registry import ConnectorRegistry, connector
from pyconnectors.exceptions import ConnectorNotFoundError


def test_registry_decorator():
    @connector("test.dummy")
    class DummyConnector(BaseConnector):
        def execute(self) -> Any:
            return "dummy"

    registered = ConnectorRegistry.get("test.dummy")
    assert registered is DummyConnector


def test_registry_not_found():
    with pytest.raises(ConnectorNotFoundError):
        ConnectorRegistry.get("non.existent")


def test_registry_list_and_clear():
    @connector("test.one")
    class One(BaseConnector):
        def execute(self):
            pass

    @connector("test.two")
    class Two(BaseConnector):
        def execute(self):
            pass

    connectors = ConnectorRegistry.list_connectors()
    assert "test.one" in connectors
    assert "test.two" in connectors

    ConnectorRegistry.clear()
    assert len(ConnectorRegistry.list_connectors()) == 0
