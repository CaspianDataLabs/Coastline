# Coastline

A Python package for declarative configuration management using Pydantic types and YAML config files.

[![PyPI Version](https://img.shields.io/pypi/v/coastline.svg)](https://pypi.org/project/coastline/)
[![Python Versions](https://img.shields.io/pypi/pyversions/coastline.svg)](https://pypi.org/project/coastline/)
[![License](https://img.shields.io/github/license/kwierman/coastline.svg)](https://github.com/kwierman/coastline/blob/main/LICENSE)

## Features

- **Type-safe configuration**: Define your configuration schemas using Pydantic models with full validation
- **YAML integration**: Load configuration from YAML files with automatic deserialization
- **Simple decorator API**: Register configuration classes with the `@config` decorator
- **Flexible registry**: Central registry for managing all your configuration classes
- **Python 3.11+**: Built for modern Python with full type hint support

## Installation

```bash
pip install coastline
```

Or using uv:

```bash
uv add coastline
```

## Quick Start

Define your configuration schemas using Pydantic models and the `@config` decorator:

```python
from coastline import config, ConfigLoader
from pydantic import BaseModel

@config
class Database(BaseModel):
    host: str
    port: int
    name: str

@config
class Cache(BaseModel):
    host: str
    port: int
    ttl: int = 300
```

Create a YAML configuration file:

```yaml
Database:
  host: localhost
  port: 5432
  name: myapp

Cache:
  host: localhost
  port: 6379
```

Load and use your configuration:

```python
loader = ConfigLoader()
config = loader.load("config.yaml")

# Access typed configuration objects
db = config["Database"]
print(f"Connecting to {db.host}:{db.port}")
```

## Usage

### The `@config` Decorator

The `@config` decorator registers your Pydantic model with the global configuration registry.

```python
from coastline import config
from pydantic import BaseModel

# Basic usage - uses class name as registry key
@config
class Database(BaseModel):
    host: str
    port: int

# With parentheses - also works
@config()
class Cache(BaseModel):
    host: str
    port: int

# Custom name for the config key
@config(name="app-settings")
class Settings(BaseModel):
    debug: bool
    log_level: str
```

### ConfigLoader

The `ConfigLoader` class loads YAML files and instantiates registered configurations.

```python
from coastline import ConfigLoader

loader = ConfigLoader()
config = loader.load("config.yaml")

# Access specific config
database = config["Database"]
print(database.host)

# Check if config exists
if "Cache" in config:
    cache = config["Cache"]
```

### Registry

The Registry provides programmatic access to registered configuration classes:

```python
from coastline import Registry

registry = Registry.get_instance()

# List all registered configs
print(registry.list())  # ['Database', 'Cache', 'Settings']

# Get a registered class
cls = registry.get("Database")
instance = cls(host="localhost", port=5432, name="test")

# Clear all registrations
registry.clear()
```

## Example Project Structure

```
myproject/
├── config.yaml
├── pyproject.toml
└── myapp/
    ├── __init__.py
    └── config.py
```

```python
# myapp/config.py
from coastline import config, ConfigLoader
from pydantic import BaseModel

@config
class Database(BaseModel):
    host: str
    port: int
    name: str
    user: str
    password: str

@config
class AppConfig(BaseModel):
    debug: bool = False
    log_level: str = "INFO"

@config
class RedisConfig(BaseModel):
    host: str
    port: int
    db: int = 0
```

```yaml
# config.yaml
Database:
  host: localhost
  port: 5432
  name: myapp
  user: admin
  password: secret

AppConfig:
  debug: true
  log_level: DEBUG

RedisConfig:
  host: localhost
  port: 6379
```

```python
# myapp/__init__.py
from coastline import ConfigLoader

_loader = ConfigLoader()
_loader.load("config.yaml")

def get_config(name: str):
    return _loader.get(name)
```

## Requirements

- Python 3.11 or higher
- pydantic >= 2.12.5
- pyyaml >= 6.0.3

## Development

```bash
# Install dependencies
uv sync

# Install dev dependencies
uv sync --group dev

# Run tests
uv run pytest

# Run linting
uv run ruff check .

# Build package
uv run python -m build
```

## License

MIT License - see LICENSE file for details.
