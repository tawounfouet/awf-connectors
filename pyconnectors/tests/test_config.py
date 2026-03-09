import json
import pytest

from pyconnectors.config import ConnectorConfig
from pyconnectors.exceptions import ConnectorConfigurationError


def test_config_from_dict():
    data = {"host": "localhost", "port": 5432}
    config = ConnectorConfig.from_dict(data)
    assert config.params["host"] == "localhost"
    assert config.params["port"] == 5432


def test_config_from_json_file(tmp_path):
    data = {"api_key": "secret123"}
    filepath = tmp_path / "config.json"
    with open(filepath, "w") as f:
        json.dump(data, f)

    config = ConnectorConfig.from_json_file(str(filepath))
    assert config.params["api_key"] == "secret123"


def test_config_from_json_file_not_found():
    with pytest.raises(ConnectorConfigurationError):
        ConnectorConfig.from_json_file("non_existent.json")


def test_config_from_env(monkeypatch):
    monkeypatch.setenv("PYCONN_DB_HOST", "db.local")
    monkeypatch.setenv("PYCONN_DB_PORT", "5432")

    config = ConnectorConfig.from_env("PYCONN_")
    assert config.params["db_host"] == "db.local"
    assert config.params["db_port"] == "5432"
