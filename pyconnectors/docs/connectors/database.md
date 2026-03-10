# Database Connectors

Database connectors enable programmatic interactions with SQL and NoSQL engines. They abstract away driver initialization logic while exposing straightforward `execute` methods.

## `database.postgresql`
**Requires:** `psycopg` (Install with `pip install pyconnectors[postgresql]`)

### Configuration
- `dsn` (str): The PostgreSQL connection string (`postgres://user:pass@host:port/db`)

### Usage
```python
config = ConnectorConfig(params={"dsn": "postgres://user:pass@localhost:5432/db"})
pg = ConnectorFactory.create("database.postgresql", config=config)

rows = pg.execute("SELECT * FROM users WHERE active = %s", (True,))
```

## `database.mysql`
**Requires:** `pymysql` (Install with `pip install pyconnectors[mysql]`)

### Configuration
- `host` (str): default `localhost`
- `port` (int): default `3306`
- `user` (str)
- `password` (str)
- `database` (str)

### Usage
```python
mysql = ConnectorFactory.create("database.mysql", config=config)
rows = mysql.execute("SELECT * FROM products")
```

## `database.sqlite`
**Requires:** None (uses stdlib `sqlite3`)

### Configuration
- `database` (str): Path to file, or `:memory:`

### Usage
```python
sqlite = ConnectorFactory.create("database.sqlite", config=config)
rows = sqlite.execute("SELECT * FROM local_data")
```

## `database.mongodb`
**Requires:** `pymongo` (Install with `pip install pyconnectors[mongodb]`)

### Configuration
- `uri` (str): e.g., `mongodb://localhost:27017/`
- `database` (str)

### Usage
```python
mongo = ConnectorFactory.create("database.mongodb", config=config)
results = mongo.execute("my_collection", "find", query={"age": {"$gt": 21}})
```

## `database.redis`
**Requires:** `redis` (Install with `pip install pyconnectors[redis]`)

### Configuration
- `url` (str): e.g., `redis://localhost:6379/0`
- or `host`, `port`, `db`

### Usage
```python
redis_conn = ConnectorFactory.create("database.redis", config=config)
redis_conn.execute("set", key="my_key", value="my_value")
val = redis_conn.execute("get", key="my_key")
```
