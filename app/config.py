from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    BOT_TOKEN: str
    DB_HOST: str
    DB_PORT: int
    DB_PASS: str
    DB_NAME: str
    DB_USER: str

    @property
    def DATABASE_URL_asyncpg(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()