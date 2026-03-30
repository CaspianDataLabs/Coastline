class Registry:
    _instance: "Registry | None" = None

    def __init__(self) -> None:
        self._classes: dict[str, type] = {}

    @classmethod
    def get_instance(cls) -> "Registry":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def register(self, name: str, cls: type) -> None:
        self._classes[name] = cls

    def get(self, name: str) -> type | None:
        return self._classes.get(name)

    def list(self) -> list[str]:
        return list(self._classes.keys())

    def clear(self) -> None:
        self._classes.clear()
