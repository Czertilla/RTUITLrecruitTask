from fastapi import FastAPI
from .config import Settings
from api.dependencies import include_routers

app = FastAPI(**Settings().app_presets)
include_routers(app)
