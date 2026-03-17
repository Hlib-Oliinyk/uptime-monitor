from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_URL: str = ""

    @model_validator(mode = "after")
    def build_db_url(self):
        self.DB_URL = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@localhost/{self.DB_NAME}"
        return self

settings = Settings()
