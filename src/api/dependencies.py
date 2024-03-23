from fastapi import FastAPI
from .routers import routers
from .auth.routers import include_routers as include_auth_routers


def include_routers(app: FastAPI) -> None:
    for router in routers:
        app.include_router(router)
    include_auth_routers(app)
