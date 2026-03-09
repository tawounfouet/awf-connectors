from typing import Any, Callable, Dict, Type

from pyconnectors.exceptions import ConnectorNotFoundError


class ConnectorRegistry:
    """Registry to dynamically keep track of available connectors."""

    _connectors: Dict[str, Type[Any]] = {}

    @classmethod
    def register(cls, name: str, connector_cls: Type[Any]) -> None:
        """Register a connector class by name."""
        cls._connectors[name] = connector_cls

    @classmethod
    def get(cls, name: str) -> Type[Any]:
        """Get a connector class by name."""
        if name not in cls._connectors:
            raise ConnectorNotFoundError(f"Connector '{name}' not found in registry.")
        return cls._connectors[name]

    @classmethod
    def list_connectors(cls) -> Dict[str, Type[Any]]:
        """List all registered connectors."""
        return cls._connectors.copy()

    @classmethod
    def clear(cls) -> None:
        """Clear the registry (useful for tests)."""
        cls._connectors.clear()


def connector(name: str) -> Callable[[Type[Any]], Type[Any]]:
    """Decorator to register a connector in the registry."""

    def wrapper(cls: Type[Any]) -> Type[Any]:
        ConnectorRegistry.register(name, cls)
        return cls

    return wrapper
