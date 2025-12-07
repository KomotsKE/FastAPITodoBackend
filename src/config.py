from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Конфигурация приложения из переменных окружения"""
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    PG_HOST: str
    PG_PORT: int
    PG_USER: str
    PG_PASSWORD: str
    PG_DB: str

    @property
    def DATABASE_URL_ASYNCPG(self) -> str:
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"


config = Config()  # type: ignore[call-arg]

