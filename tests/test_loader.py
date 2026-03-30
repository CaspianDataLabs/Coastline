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


@pytest.fixture
def registered_configs():
    class Database(BaseModel):
        host: str
        port: int
        name: str

    class Server(BaseModel):
        host: str
        port: int

    @config(name="Database")
    class _Database(Database):
        pass

    @config(name="Server")
    class _Server(Server):
        pass

    return {"Database": Database, "Server": Server}


class TestConfigLoader:
    def test_load_valid_yaml(self, temp_yaml_file, registered_configs):
        temp_yaml_file.write_text("""
Database:
  host: localhost
  port: 5432
  name: mydb
""")
        loader = ConfigLoader()
        result = loader.load(temp_yaml_file)

        assert "Database" in result
        assert result["Database"].host == "localhost"
        assert result["Database"].port == 5432
        assert result["Database"].name == "mydb"

    def test_load_multiple_configs(self, temp_yaml_file, registered_configs):
        temp_yaml_file.write_text("""
Database:
  host: db.example.com
  port: 5432
  name: production

Server:
  host: 0.0.0.0
  port: 8080
""")
        loader = ConfigLoader()
        result = loader.load(temp_yaml_file)

        assert result["Database"].host == "db.example.com"
        assert result["Server"].host == "0.0.0.0"
        assert result["Server"].port == 8080

    def test_load_unregistered_key_returns_raw_dict(
        self, temp_yaml_file, registered_configs
    ):
        temp_yaml_file.write_text("""
Unregistered:
  value: test
""")
        loader = ConfigLoader()
        result = loader.load(temp_yaml_file)

        assert result["Unregistered"] == {"value": "test"}

    def test_load_empty_yaml(self, temp_yaml_file, registered_configs):
        temp_yaml_file.write_text("")
        loader = ConfigLoader()
        result = loader.load(temp_yaml_file)

        assert result == {}

    def test_load_only_comments(self, temp_yaml_file, registered_configs):
        temp_yaml_file.write_text("# just a comment")
        loader = ConfigLoader()
        result = loader.load(temp_yaml_file)

        assert result == {}

    def test_get_returns_loaded_instance(self, temp_yaml_file, registered_configs):
        temp_yaml_file.write_text("""
Database:
  host: localhost
  port: 5432
  name: testdb
""")
        loader = ConfigLoader()
        loader.load(temp_yaml_file)

        db = loader.get("Database")
        assert db is not None
        assert db.host == "localhost"

    def test_get_nonexistent_returns_none(self, temp_yaml_file, registered_configs):
        temp_yaml_file.write_text(
            "Database:\n  host: localhost\n  port: 5432\n  name: db"
        )
        loader = ConfigLoader()
        loader.load(temp_yaml_file)

        assert loader.get("NonExistent") is None

    def test_load_replaces_previous_instances(self, temp_yaml_file, registered_configs):
        temp_yaml_file.write_text("Database:\n  host: first\n  port: 5432\n  name: db")
        loader = ConfigLoader()
        loader.load(temp_yaml_file)

        temp_yaml_file.write_text("Database:\n  host: second\n  port: 5432\n  name: db")
        loader.load(temp_yaml_file)

        assert loader.get("Database").host == "second"

    def test_load_with_string_path(self, temp_yaml_file, registered_configs):
        temp_yaml_file.write_text(
            "Database:\n  host: localhost\n  port: 5432\n  name: db"
        )
        loader = ConfigLoader()
        result = loader.load(str(temp_yaml_file))

        assert "Database" in result

    def test_load_with_pathlib_path(self, temp_yaml_file, registered_configs):
        temp_yaml_file.write_text(
            "Database:\n  host: localhost\n  port: 5432\n  name: db"
        )
        loader = ConfigLoader()
        result = loader.load(temp_yaml_file)

        assert "Database" in result
