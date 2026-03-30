# Quick Start

This guide will walk you through the basics of using Coastline to manage your application configuration.

## Step 1: Define Configuration Models

Create a Python file (e.g., `config.py`) and define your configuration schemas using Pydantic models with the `@config` decorator:

```python
from coastline import config
from pydantic import BaseModel

@config
class Database(BaseModel):
    host: str
    port: int
    name: str
    user: str
    password: str

@config
class RedisConfig(BaseModel):
    host: str
    port: int
    db: int = 0  # Default value

@config
class AppSettings(BaseModel):
    debug: bool = False
    log_level: str = "INFO"
    max_connections: int = 100
```

## Step 2: Create a YAML Configuration File

Create a `config.yaml` file in your project root:

```yaml
Database:
  host: localhost
  port: 5432
  name: myapp
  user: admin
  password: secret

RedisConfig:
  host: localhost
  port: 6379
  db: 0

AppSettings:
  debug: true
  log_level: DEBUG
  max_connections: 50
```

## Step 3: Load Configuration

Use the `ConfigLoader` to load your configuration:

```python
from coastline import ConfigLoader

loader = ConfigLoader()
config = loader.load("config.yaml")

# Access typed configuration objects
database = config["Database"]
redis = config["RedisConfig"]
settings = config["AppSettings"]

print(f"Connecting to database at {database.host}:{database.port}")
print(f"Debug mode: {settings.debug}")
```

## Using Custom Names

If you want to use a different key name in YAML than your class name, use the `name` parameter:

```python
@config(name="app-config")
class AppConfiguration(BaseModel):
    version: str
    environment: str
```

```yaml
app-config:
  version: "1.0.0"
  environment: "production"
```

## Working with Multiple Config Files

You can load configurations from multiple files:

```python
from coastline import ConfigLoader

loader = ConfigLoader()
base_config = loader.load("base.yaml")

# Merge additional config
loader.load("local.yaml")

# Access all loaded configs
all_configs = loader.load("config.yaml")
```

## Next Steps

- Learn about [Configuration Basics](../guide/configuration-basics.md) for more advanced patterns
- Explore the [Registry](../guide/registry.md) for programmatic configuration management
