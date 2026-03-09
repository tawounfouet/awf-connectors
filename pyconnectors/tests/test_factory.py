import pytest
from typing import Any
from pyconnectors.base import BaseConnector
from pyconnectors.config import ConnectorConfig
from pyconnectors.factory import ConnectorFactory
from pyconnectors.registry import connector
from pyconnectors.exceptions import ConnectorConfigurationError


from pyconnectors.registry import ConnectorRegistry

class FactoryTestConnector(BaseConnector):
    def execute(self) -> Any:
        return self.config.params.get("value")


@pytest.fixture(autouse=True)
def register_test_connector():
    ConnectorRegistry.register("factory.test", FactoryTestConnector)
    yield


def test_factory_create_with_dict():
    conn = ConnectorFactory.create("factory.test", config_dict={"value": 42})
    assert conn.execute() == 42
    assert isinstance(conn.config, ConnectorConfig)


def test_factory_create_with_config():
    config = ConnectorConfig(params={"value": 100})
    conn = ConnectorFactory.create("factory.test", config=config)
    assert conn.execute() == 100
    assert conn.config is config


def test_factory_create_without_config():
    conn = ConnectorFactory.create("factory.test")
    assert conn.execute() is None


def test_factory_create_with_invalid_config_cls():
    class BrokenConfig:
        @classmethod
        def from_dict(cls, data):
            raise ValueError("Broken")

    with pytest.raises(ConnectorConfigurationError):
        ConnectorFactory.create("factory.test", config_cls=BrokenConfig)
