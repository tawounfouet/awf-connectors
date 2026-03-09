from typing import Any, Dict, Optional, Type, cast

from pyconnectors.base import BaseConnector
from pyconnectors.config import ConnectorConfig
from pyconnectors.exceptions import ConnectorConfigurationError
from pyconnectors.registry import ConnectorRegistry


class ConnectorFactory:
    """Factory for creating connector instances."""

    @classmethod
    def create(
        cls,
        name: str,
        config: Optional[ConnectorConfig] = None,
        config_dict: Optional[Dict[str, Any]] = None,
        config_cls: Optional[Type[ConnectorConfig]] = None,
    ) -> BaseConnector:
        """
        Create a connector by name from the registry and inject its configuration.
        """
        connector_cls = cast(Type[BaseConnector], ConnectorRegistry.get(name))

        if config is None:
            if config_dict is None:
                config_dict = {}
            if config_cls is None:
                config_cls = ConnectorConfig
            try:
                config = config_cls.from_dict(config_dict)
            except Exception as e:
                raise ConnectorConfigurationError(f"Failed to load connector config: {e}")

        return connector_cls(config)
