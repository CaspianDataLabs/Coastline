from .registry import Registry


def config(cls: type | None = None, *, name: str | None = None):
    """Decorator to register a class with the config registry."""

    def decorator(cls_: type) -> type:
        key = name or cls_.__name__
        Registry.get_instance().register(key, cls_)
        return cls_

    if cls is not None:
        return decorator(cls)
    return decorator
