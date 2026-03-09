"""PyConnectors: A universal framework for accessing external services."""

from pyconnectors.base import BaseConnector
from pyconnectors.config import ConnectorConfig
from pyconnectors.exceptions import (
    ConnectorConfigurationError,
    ConnectorExecutionError,
    ConnectorNotFoundError,
    PyConnectorsError,
)
from pyconnectors.factory import ConnectorFactory
from pyconnectors.registry import ConnectorRegistry, connector
from pyconnectors.result import ConnectorResult

__version__ = "0.1.0"

__all__ = [
    "BaseConnector",
    "ConnectorConfig",
    "ConnectorFactory",
    "ConnectorRegistry",
    "connector",
    "ConnectorResult",
    "PyConnectorsError",
    "ConnectorNotFoundError",
    "ConnectorConfigurationError",
    "ConnectorExecutionError",
]
