from coastline import Registry


class TestRegistry:
    def test_singleton_returns_same_instance(self):
        instance1 = Registry.get_instance()
        instance2 = Registry.get_instance()
        assert instance1 is instance2

    def test_register_and_get(self, sample_config):
        registry = Registry.get_instance()
        Database = sample_config["Database"]

        registry.register("Database", Database)

        assert registry.get("Database") is Database

    def test_get_nonexistent_returns_none(self):
        registry = Registry.get_instance()
        assert registry.get("NonExistent") is None

    def test_list_returns_registered_keys(self, sample_config):
        registry = Registry.get_instance()
        Database = sample_config["Database"]
        Server = sample_config["Server"]

        registry.register("Database", Database)
        registry.register("Server", Server)

        keys = registry.list()
        assert "Database" in keys
        assert "Server" in keys
        assert len(keys) == 2

    def test_list_empty_for_fresh_registry(self):
        registry = Registry.get_instance()
        assert registry.list() == []

    def test_clear_removes_all_entries(self, sample_config):
        registry = Registry.get_instance()
        Database = sample_config["Database"]

        registry.register("Database", Database)
        registry.clear()

        assert registry.get("Database") is None
        assert registry.list() == []

    def test_register_overwrites_existing(self, sample_config):
        registry = Registry.get_instance()
        Database = sample_config["Database"]
        Server = sample_config["Server"]

        registry.register("Config", Database)
        registry.register("Config", Server)

        assert registry.get("Config") is Server

    def test_multiple_classes_same_module(self, sample_config):
        registry = Registry.get_instance()

        registry.register("Database", sample_config["Database"])
        registry.register("Server", sample_config["Server"])

        assert registry.get("Database") is sample_config["Database"]
        assert registry.get("Server") is sample_config["Server"]
        assert len(registry.list()) == 2
