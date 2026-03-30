import pytest
from coastline import Registry
from pydantic import BaseModel


@pytest.fixture(autouse=True)
def clean_registry():
    Registry.get_instance().clear()
    yield
    Registry.get_instance().clear()


@pytest.fixture
def sample_config():
    class Database(BaseModel):
        host: str
        port: int
        name: str

    class Server(BaseModel):
        host: str
        port: int

    return {"Database": Database, "Server": Server}
