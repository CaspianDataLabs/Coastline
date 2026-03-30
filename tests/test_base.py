from coastline import config, Registry
from pydantic import BaseModel


class TestConfigDecorator:
    def test_decorator_with_class_name(self):
        registry = Registry.get_instance()

        @config
        class MyConfig(BaseModel):
            value: str

        assert registry.get("MyConfig") is MyConfig
        assert MyConfig.__name__ == "MyConfig"

    def test_decorator_with_custom_name(self):
        registry = Registry.get_instance()

        @config(name="CustomName")
        class AnotherConfig(BaseModel):
            value: str

        assert registry.get("CustomName") is AnotherConfig
        assert registry.get("AnotherConfig") is None

    def test_decorator_without_parentheses(self):
        registry = Registry.get_instance()

        @config
        class SimpleConfig(BaseModel):
            name: str

        assert registry.get("SimpleConfig") is SimpleConfig

    def test_decorator_with_parentheses_no_args(self):
        registry = Registry.get_instance()

        @config()
        class ParenConfig(BaseModel):
            name: str

        assert registry.get("ParenConfig") is ParenConfig

    def test_decorator_preserves_class_functionality(self):
        @config
        class UserConfig(BaseModel):
            host: str
            port: int

        user = UserConfig(host="localhost", port=5432)
        assert user.host == "localhost"
        assert user.port == 5432

    def test_decorator_multiple_classes(self):
        registry = Registry.get_instance()

        @config
        class First(BaseModel):
            pass

        @config
        class Second(BaseModel):
            pass

        assert registry.get("First") is First
        assert registry.get("Second") is Second
        assert len(registry.list()) == 2

    def test_decorator_registers_with_kebab_case_name(self):
        registry = Registry.get_instance()

        @config(name="my-config")
        class KebabConfig(BaseModel):
            value: str

        assert registry.get("my-config") is KebabConfig
