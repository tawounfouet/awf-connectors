class PyConnectorsError(Exception):
    """Base exception for all PyConnectors errors."""

    pass


class ConnectorNotFoundError(PyConnectorsError):
    """Raised when a connector is not found in the registry."""

    pass


class ConnectorConfigurationError(PyConnectorsError):
    """Raised when there is an issue with connector configuration."""

    pass


class ConnectorExecutionError(PyConnectorsError):
    """Raised when a connector fails to execute."""

    pass
