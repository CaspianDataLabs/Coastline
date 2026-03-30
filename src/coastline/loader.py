from pathlib import Path
import yaml
from typing import Any
from .registry import Registry


class ConfigLoader:
    def __init__(self) -> None:
        self._instances: dict[str, Any] = {}

    def load(self, path: str | Path) -> dict[str, Any]:
        path = Path(path)
        data = yaml.safe_load(path.read_text()) or {}

        registry = Registry.get_instance()
        self._instances = {}

        for key, value in data.items():
            cls = registry.get(key)
            if cls is not None:
                self._instances[key] = cls(**value)
            else:
                self._instances[key] = value

        return self._instances

    def get(self, name: str) -> Any:
        return self._instances.get(name)
