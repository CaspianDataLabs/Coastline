# Configuration Basics

This guide covers the fundamental concepts of defining configurations with Coastline.

## The `@config` Decorator

The `@config` decorator registers your Pydantic model with the global configuration registry. This allows the `ConfigLoader` to automatically instantiate your configuration classes.

### Basic Usage

```python
from coastline import config
from pydantic import BaseModel

@config
class MyConfig(BaseModel):
    key: str
```

The class name (`MyConfig`) is used as the registry key.

### With Parentheses

```python
@config()
class AnotherConfig(BaseModel):
    setting: int
```

### Custom Names

Use the `name` parameter to specify a different registry key:

```python
@config(name="custom-key")
class CustomConfig(BaseModel):
    value: str
```

## Pydantic Model Features

Since your configuration classes are Pydantic models, you get all Pydantic features:

### Type Validation

```python
@config
class ValidatedConfig(BaseModel):
    port: int  # Will be validated as integer
    ratio: float  # Will be validated as float
    enabled: bool  # Will be validated as boolean
```

### Default Values

```python
@config
class ConfigWithDefaults(BaseModel):
    host: str = "localhost"
    port: int = 8080
    debug: bool = False
```

### Field Validation

```python
from pydantic import Field
from coastline import config

@config
class ValidatedFields(BaseModel):
    port: int = Field(ge=1, le=65535, description="Port number")
    name: str = Field(min_length=1, max_length=100)
    timeout: float = Field(gt=0, description="Timeout in seconds")
```

### Nested Models

```python
from coastline import config

@config
class DatabaseConfig(BaseModel):
    host: str
    port: int

@config
class AppConfig(BaseModel):
    database: DatabaseConfig
    debug: bool
```

```yaml
AppConfig:
  database:
    host: localhost
    port: 5432
  debug: true
```

## Configuration Patterns

### Environment-Specific Configs

```python
@config
class DevelopmentConfig(BaseModel):
    debug: bool = True
    log_level: str = "DEBUG"

@config
class ProductionConfig(BaseModel):
    debug: bool = False
    log_level: str = "WARNING"
```

### Configuration Inheritance

```python
from pydantic import BaseModel

class BaseDatabaseConfig(BaseModel):
    host: str
    port: int
    timeout: int = 30

from coastline import config

@config
class PostgreSQLConfig(BaseDatabaseConfig):
    database: str
    pool_size: int = 10

@config
class MySQLConfig(BaseDatabaseConfig):
    charset: str = "utf8mb4"
```

## Best Practices

1. **Use descriptive names**: Choose clear, descriptive names for your configuration classes
2. **Group related configs**: Organize related settings into logical groups
3. **Provide defaults**: Use default values for optional settings
4. **Document fields**: Use field descriptions for configuration documentation
5. **Validate inputs**: Use Pydantic validators for complex validation logic
