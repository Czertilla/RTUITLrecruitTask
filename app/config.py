from pydantic_settings import BaseSettings, SettingsConfigDict

from utils.singleton import Singleton
from .contextmanager import lifespan
from routers import routers

class Settings(BaseSettings, Singleton):
    app_name: str = "Lizzard Dungeon Master"
    app_presets: dict ={
        'title': app_name,
        'lifespan': lifespan
    }

    # model_config = SettingsConfigDict(env_file=".env")

