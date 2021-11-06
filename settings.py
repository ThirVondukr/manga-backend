from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    class Config:
        env_prefix = "db_"

    driver: str
    database: str
    username: str
    password: str
    host: str

    echo: bool

    @property
    def url(self) -> str:
        return f"{self.driver}://{self.username}:{self.password}@{self.host}/{self.database}"


class TestDatabaseSettings(BaseSettings):
    class Config:
        env_prefix = "test_db_"

    sync_driver: str
    driver: str
    username: str
    password: str
    host: str

    def get_sync_database_url(self, database_name: str) -> str:
        return f"{self.sync_driver}://{self.username}:{self.password}@{self.host}/{database_name}"

    def get_database_url(self, database_name: str) -> str:
        return f"{self.driver}://{self.username}:{self.password}@{self.host}/{database_name}"


class AuthSettings(BaseSettings):
    class Config:
        env_prefix = "auth_"

    secret_key: str
    algorithm: str
    token_lifetime_min: int


database = DatabaseSettings(_env_file=".env")
test_database = TestDatabaseSettings(_env_file=".env")
auth = AuthSettings(_env_file=".env")
