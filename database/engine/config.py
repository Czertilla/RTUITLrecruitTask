
from pydantic_settings import BaseSettings, SettingsConfigDict
from utils.singleton import Singleton

class Settings(BaseSettings, Singleton):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_DBMS: str = "sqlite"
    USERS_SECTRET: str
    PASSW_SECTRET: str

    model_config = SettingsConfigDict(env_file=".env")
