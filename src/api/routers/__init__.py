from .cameras import cameras
from .specialists import specialists
from .managers import managers
routers = (
    cameras,
    specialists,
    managers,
)

from fastapi import FastAPI
from api.auth.routers import include_routers as include_auth_routers

def include_routers(app: FastAPI) -> None:
    for router in routers:
        app.include_router(router)
    include_auth_routers(app)

