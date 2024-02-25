from typing import Annotated
from fastapi import FastAPI
from .config import get_settings
from routers import include_routers
__all__ = ['app']

app = FastAPI(**get_settings().app_presets)
include_routers(app)
