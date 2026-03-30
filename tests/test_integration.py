import pytest
import tempfile
from pathlib import Path
from coastline import config, ConfigLoader
from pydantic import BaseModel


@pytest.fixture
def temp_yaml_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yield Path(f.name)
    Path(f.name).unlink(missing_ok=True)


class TestIntegration:
    def test_full_workflow(self, temp_yaml_file):
        @config
        class Database(BaseModel):
            host: str
            port: int
            name: str

        @config
        class Cache(BaseModel):
            host: str
            ttl: int

        temp_yaml_file.write_text("""
Database:
  host: db.example.com
  port: 5432
  name: myapp

Cache:
  host: redis.example.com
  ttl: 3600
""")
        loader = ConfigLoader()
        loaded_config = loader.load(temp_yaml_file)

        assert loaded_config["Database"].host == "db.example.com"
        assert loaded_config["Database"].port == 5432
        assert loaded_config["Cache"].host == "redis.example.com"
        assert loaded_config["Cache"].ttl == 3600

    def test_mixed_registered_and_unregistered(self, temp_yaml_file):
        @config(name="Database")
        class Database(BaseModel):
            host: str
            port: int

        temp_yaml_file.write_text("""
Database:
  host: localhost
  port: 5432

Logging:
  level: INFO
  format: json
""")
        loader = ConfigLoader()
        loaded_config = loader.load(temp_yaml_file)

        assert isinstance(loaded_config["Database"], Database)
        assert loaded_config["Logging"] == {"level": "INFO", "format": "json"}

    def test_registry_state_after_multiple_loads(self, temp_yaml_file):
        @config
        class ConfigA(BaseModel):
            value: str

        @config
        class ConfigB(BaseModel):
            value: int

        temp_yaml_file.write_text("ConfigA:\n  value: first")
        loader1 = ConfigLoader()
        result1 = loader1.load(temp_yaml_file)

        temp_yaml_file.write_text("ConfigB:\n  value: 42")
        loader2 = ConfigLoader()
        result2 = loader2.load(temp_yaml_file)

        assert result1["ConfigA"].value == "first"
        assert result2["ConfigB"].value == 42
        assert "ConfigA" not in result2

    def test_decorator_with_custom_names_integration(self, temp_yaml_file):
        @config(name="db_config")
        class Database(BaseModel):
            host: str

        @config(name="server_config")
        class Server(BaseModel):
            port: int

        temp_yaml_file.write_text("""
db_config:
  host: database.local

server_config:
  port: 8080
""")
        loader = ConfigLoader()
        loaded_config = loader.load(temp_yaml_file)

        assert loaded_config["db_config"].host == "database.local"
        assert loaded_config["server_config"].port == 8080

    def test_empty_registry_with_yaml_data(self, temp_yaml_file):
        temp_yaml_file.write_text("""
UnknownConfig:
  key: value
""")
        loader = ConfigLoader()
        config = loader.load(temp_yaml_file)

        assert config["UnknownConfig"] == {"key": "value"}

    def test_multiple_loaders_independent_instances(self, temp_yaml_file):
        @config
        class Config(BaseModel):
            value: str

        temp_yaml_file.write_text("Config:\n  value: original")
        loader1 = ConfigLoader()
        result1 = loader1.load(temp_yaml_file)

        loader2 = ConfigLoader()
        result2 = loader2.load(temp_yaml_file)

        assert result1["Config"].value == "original"
        assert result2["Config"].value == "original"
        assert result1["Config"] is not result2["Config"]
