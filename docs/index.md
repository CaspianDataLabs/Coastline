# Coastline

Welcome to the **Coastline** documentation! Coastline is a Python package for declarative configuration management using Pydantic types and YAML config files.

## What is Coastline?

Coastline provides a simple, type-safe way to manage application configuration:

- **Define** your configuration schemas as Pydantic models
- **Register** them with the `@config` decorator
- **Load** values from YAML files with automatic validation

## Features

- **Type-safe configuration** - Define schemas with Pydantic for automatic validation
- **YAML integration** - Load configuration from YAML files
- **Simple API** - Just decorate your classes and load
- **Flexible registry** - Manage configuration classes programmatically

## Quick Example

```python
from coastline import config, ConfigLoader
from pydantic import BaseModel

@config
class Database(BaseModel):
    host: str
    port: int
    name: str

# config.yaml:
# Database:
#   host: localhost
#   port: 5432
#   name: myapp

loader = ConfigLoader()
cfg = loader.load("config.yaml")
print(cfg["Database"].host)  # "localhost"
```

## Navigation

- [Getting Started](getting-started/installation.md) - Install and set up Coastline
- [Quick Start](getting-started/quick-start.md) - Build your first configuration
- [Configuration Guide](guide/configuration-basics.md) - Deep dive into configuration patterns
- [API Reference](api.md) - Complete API documentation

## License

Coastline is released under the MIT License.
