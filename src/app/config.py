from pydantic_settings import BaseSettings, SettingsConfigDict

from utils.singleton import Singleton
from .contextmanager import lifespan

class Settings(BaseSettings, Singleton):
    app_name: str = "Lizzard Dungeon Master"
    app_presets: dict ={
        'title': app_name,
        'lifespan': lifespan
    }

    DB_HOST: str|None
    DB_PORT: str|None
    DB_NAME: str|None
    DB_USER: str|None
    DB_PASS: str|None
    DB_DBMS: str = "sqlite"
    USERS_SECTRET: str
    PASSW_SECTRET: str

    model_config = SettingsConfigDict(env_file=".env")
