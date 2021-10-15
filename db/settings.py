from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    class Config:
        env_prefix = "db_"

    database_url: str
    echo: bool


database_settings = DatabaseSettings()
