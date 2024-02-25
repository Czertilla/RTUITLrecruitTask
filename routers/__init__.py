from fastapi import FastAPI
from .cameras import cameras
from .specialists import specialists
from .managers import managers

routers = (
    cameras,
    specialists,
    managers
)

def include_routers(app: FastAPI) -> None:
    for router in routers:
        app.include_router(router)
