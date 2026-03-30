from coastline import config, ConfigLoader
from pydantic import BaseModel


@config
class Database(BaseModel):
    host: str
    port: int
    name: str


@config
class Server(BaseModel):
    host: str
    port: int


if __name__ == "__main__":
    loader = ConfigLoader()
    cfg = loader.load("config.yaml")

    print(f"Database host: {cfg['Database'].host}")
    print(f"Database port: {cfg['Database'].port}")
    print(f"Server host: {cfg['Server'].host}")
    print(f"Server port: {cfg['Server'].port}")
