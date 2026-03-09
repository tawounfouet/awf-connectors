import pytest
from unittest.mock import MagicMock, patch

from pyconnectors.config import ConnectorConfig
from pyconnectors.connectors.database.postgresql import PostgreSQLConnector


@pytest.fixture
def pg_connector():
    config = ConnectorConfig(params={"dsn": "postgres://user:pass@localhost:5432/db"})
    return PostgreSQLConnector(config)


@patch("pyconnectors.connectors.database.postgresql.psycopg")
def test_pg_connector_execute(mock_psycopg, pg_connector):
    if mock_psycopg is None:
        pytest.skip("psycopg not available")

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Setup context managers
    mock_psycopg.connect.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [("row1",), ("row2",)]

    result = pg_connector.execute("SELECT * FROM table")

    assert result == [("row1",), ("row2",)]
    mock_psycopg.connect.assert_called_with("postgres://user:pass@localhost:5432/db")
    mock_cursor.execute.assert_called_with("SELECT * FROM table", None)


@patch("pyconnectors.connectors.database.postgresql.psycopg")
def test_pg_connector_no_dsn(mock_psycopg):
    if mock_psycopg is None:
        pytest.skip("psycopg not available")

    config = ConnectorConfig()
    connector = PostgreSQLConnector(config)
    with pytest.raises(ValueError):
        connector.execute("SELECT 1")
