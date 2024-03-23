from fastapi import FastAPI
from .routers import routers
from .auth.routers import include_routers


def include_routers(app: FastAPI) -> None:
    for router in routers:
        app.include_router(router)
    include_routers(app)
