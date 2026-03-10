import pytest
from unittest.mock import MagicMock, patch

from pyconnectors.config import ConnectorConfig
from pyconnectors.connectors.database.mongodb import MongoDBConnector
from pyconnectors.connectors.database.mysql import MySQLConnector
from pyconnectors.connectors.database.postgresql import PostgreSQLConnector
from pyconnectors.connectors.database.redis import RedisConnector
from pyconnectors.connectors.database.sqlite import SQLiteConnector


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


@patch("pyconnectors.connectors.database.mysql.pymysql")
def test_mysql_connector_execute(mock_pymysql):
    if mock_pymysql is None:
        pytest.skip("pymysql not available")

    config = ConnectorConfig(
        params={
            "host": "localhost",
            "user": "root",
            "password": "pwd",
            "database": "testdb",
        }
    )
    connector = MySQLConnector(config)

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_pymysql.connect.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [{"col": "val1"}, {"col": "val2"}]

    result = connector.execute("SELECT * FROM table")

    assert result == [{"col": "val1"}, {"col": "val2"}]
    mock_pymysql.connect.assert_called_with(
        host="localhost",
        port=3306,
        user="root",
        password="pwd",
        database="testdb",
        cursorclass=mock_pymysql.cursors.DictCursor,
    )
    mock_cursor.execute.assert_called_with("SELECT * FROM table", None)


@patch("pyconnectors.connectors.database.mongodb.pymongo")
def test_mongodb_connector_execute(mock_pymongo):
    if mock_pymongo is None:
        pytest.skip("pymongo not available")

    config = ConnectorConfig(params={"uri": "mongodb://localhost:27017/", "database": "testdb"})
    connector = MongoDBConnector(config)

    mock_client = MagicMock()
    mock_db = MagicMock()
    mock_col = MagicMock()

    mock_pymongo.MongoClient.return_value = mock_client
    mock_client.__getitem__.return_value = mock_db
    mock_db.__getitem__.return_value = mock_col

    mock_col.find.return_value = [{"_id": "1", "name": "doc1"}]

    result = connector.execute("mycol", "find", query={"name": "doc1"})

    assert result == [{"_id": "1", "name": "doc1"}]
    mock_pymongo.MongoClient.assert_called_with("mongodb://localhost:27017/")
    mock_client.__getitem__.assert_called_with("testdb")
    mock_db.__getitem__.assert_called_with("mycol")
    mock_col.find.assert_called_with({"name": "doc1"})


@patch("pyconnectors.connectors.database.redis.redis")
def test_redis_connector_execute(mock_redis):
    if mock_redis is None:
        pytest.skip("redis not available")

    config = ConnectorConfig(params={"host": "localhost", "port": 6379, "db": 0})
    connector = RedisConnector(config)

    mock_client = MagicMock()
    mock_redis.Redis.return_value = mock_client
    mock_client.get.return_value = b"myvalue"

    result = connector.execute("get", key="mykey")

    assert result == "myvalue"
    mock_redis.Redis.assert_called_with(host="localhost", port=6379, db=0)
    mock_client.get.assert_called_with("mykey")


@patch("pyconnectors.connectors.database.sqlite.sqlite3")
def test_sqlite_connector_execute(mock_sqlite3):
    config = ConnectorConfig(params={"database": ":memory:"})
    connector = SQLiteConnector(config)

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_sqlite3.connect.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [{"col": "val1"}]

    result = connector.execute("SELECT * FROM table")

    assert result == [{"col": "val1"}]
    mock_sqlite3.connect.assert_called_with(":memory:")
    mock_cursor.execute.assert_called_with("SELECT * FROM table", ())
