# ConfigLoader

The `ConfigLoader` class handles loading configuration from YAML files and instantiating registered configurations.

## Overview

```python
from coastline import ConfigLoader
```

## Methods

### `__init__()`

Creates a new ConfigLoader instance.

```python
loader = ConfigLoader()
```

### `load(path)`

Loads configuration from a YAML file.

**Parameters:**

- `path` (str | Path): Path to the YAML configuration file

**Returns:**

- `dict[str, Any]`: Dictionary mapping config names to instantiated Pydantic models

```python
loader = ConfigLoader()
config = loader.load("config.yaml")
```

### `get(name)`

Retrieves a previously loaded configuration by name.

**Parameters:**

- `name` (str): Name of the configuration

**Returns:**

- The instantiated configuration object, or None if not found

```python
config = loader.get("Database")
if config:
    print(config.host)
```

## Loading Behavior

1. Reads the YAML file using `yaml.safe_load()`
2. For each key in the YAML:
   - If a matching class is registered, instantiates it with the YAML values
   - Otherwise, returns the raw YAML value

```python
# YAML with mixed registered and unregistered keys
@config
class Database(BaseModel):
    host: str
    port: int

# YAML:
# Database:
#   host: localhost
#   port: 5432
# custom_data:
#   value: 42
```

```python
loader = ConfigLoader()
config = loader.load("config.yaml")

# Database is a Pydantic instance
db = config["Database"]
print(type(db))  # <class 'Database'>

# Unregistered keys return raw values
custom = config["custom_data"]
print(type(custom))  # <class 'dict'>
```

## Example: Complete Usage

```python
from coastline import config, ConfigLoader
from pydantic import BaseModel

@config
class Database(BaseModel):
    host: str
    port: int
    name: str

@config
class Redis(BaseModel):
    host: str
    port: int

# Load configuration
loader = ConfigLoader()
config = loader.load("config.yaml")

# Use configurations
db = config["Database"]
redis = config["Redis"]

# Database connection
print(f"Connecting to {db.host}:{db.port}/{db.name}")

# Redis connection
print(f"Redis at {redis.host}:{redis.port}")
```

## Error Handling

If the YAML file contains invalid data for a registered model, Pydantic validation will raise an error:

```python
try:
    config = loader.load("config.yaml")
except ValidationError as e:
    print(f"Configuration error: {e}")
```
