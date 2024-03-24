from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str|None
    DB_PORT: str|None
    DB_NAME: str|None
    DB_USER: str|None
    DB_PASS: str|None
    DB_DBMS: str = "sqlite"
    USERS_SECTRET: str
    PASSW_SECTRET: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def getSettings():
    return Settings()