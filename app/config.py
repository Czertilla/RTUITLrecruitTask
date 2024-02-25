from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from routers import routers
__all__ = ['get_settings']

class Settings(BaseSettings):
    app_name: str = "Lizzard Dungeon Master"
    app_presets: dict ={
        'title': app_name
    }

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()
