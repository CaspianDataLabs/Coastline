# Registry

The Registry provides a singleton-based mechanism for managing registered configuration classes.

## Overview

```python
from coastline import Registry
```

## Singleton Pattern

The Registry uses a singleton pattern to ensure only one registry instance exists:

```python
registry1 = Registry.get_instance()
registry2 = Registry.get_instance()

print(registry1 is registry2)  # True
```

## Methods

### `get_instance()`

Returns the singleton Registry instance.

```python
registry = Registry.get_instance()
```

### `register(name, cls)`

Registers a configuration class with a given name.

**Parameters:**

- `name` (str): The key to register the class under
- `cls` (type): The class to register

```python
from coastline import Registry, config
from pydantic import BaseModel

registry = Registry.get_instance()

@config
class Database(BaseModel):
    host: str
    port: int

# Or register manually
registry.register("Database", Database)
```

### `get(name)`

Retrieves a registered class by name.

**Parameters:**

- `name` (str): The key of the class to retrieve

**Returns:**

- The registered class, or None if not found

```python
cls = registry.get("Database")
if cls:
    instance = cls(host="localhost", port=5432)
```

### `list()`

Lists all registered configuration keys.

**Returns:**

- `list[str]`: List of all registered key names

```python
keys = registry.list()
print(keys)  # ['Database', 'Cache', 'Settings']
```

### `clear()`

Clears all registered configurations.

```python
registry.clear()
print(registry.list())  # []
```

## Usage with `@config` Decorator

The `@config` decorator uses the Registry internally:

```python
from coastline import config, Registry

@config
class Database(BaseModel):
    host: str
    port: int

# Equivalent to:
# Registry.get_instance().register("Database", Database)
```

## Programmatic Access

You can use the Registry directly for more control:

```python
from coastline import Registry

registry = Registry.get_instance()

# Register classes manually
class Database(BaseModel):
    host: str
    port: int

registry.register("DB", Database)

# Later, get the class
cls = registry.get("DB")
```

## Testing

The Registry can be cleared between tests:

```python
import pytest
from coastline import Registry

@pytest.fixture(autouse=True)
def clean_registry():
    Registry.get_instance().clear()
    yield
    Registry.get_instance().clear()
```

## Best Practices

1. **Use `@config` decorator** for most cases - it handles registration automatically
2. **Use Registry directly** for dynamic class registration
3. **Clear registry in tests** to ensure test isolation
4. **Use descriptive names** to avoid conflicts
