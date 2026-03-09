import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict

from pyconnectors.exceptions import ConnectorConfigurationError


@dataclass
class ConnectorConfig:
    """Base configuration for all connectors."""

    # Extra parameters dynamically loaded
    params: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConnectorConfig":
        """Load configuration from a dictionary."""
        # Simple extraction to avoid throwing TypeError on unknown fields
        known_fields = {f.name for f in cls.__dataclass_fields__.values() if f.name != "params"}
        params = {}
        init_kwargs = {}

        for k, v in data.items():
            if k in known_fields:
                init_kwargs[k] = v
            else:
                params[k] = v

        return cls(**init_kwargs, params=params)

    @classmethod
    def from_json_file(cls, filepath: str) -> "ConnectorConfig":
        """Load configuration from a JSON file."""
        if not os.path.exists(filepath):
            raise ConnectorConfigurationError(f"Configuration file not found: {filepath}")

        try:
            with open(filepath, "r") as f:
                data = json.load(f)
            return cls.from_dict(data)
        except json.JSONDecodeError as e:
            raise ConnectorConfigurationError(f"Invalid JSON configuration file: {e}")

    @classmethod
    def from_env(cls, prefix: str) -> "ConnectorConfig":
        """Load configuration from environment variables with a specific prefix."""
        data = {}
        for key, value in os.environ.items():
            if key.startswith(prefix):
                # Remove prefix and convert to lowercase for the dict key
                k = key[len(prefix) :].lower()
                data[k] = value

        return cls.from_dict(data)
