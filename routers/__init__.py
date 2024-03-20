from fastapi import FastAPI
from app.auth.auth import fastapi_users, auth_backend
from schemas.auth import UserCreate, UserRead, UserUpdate
from .cameras import cameras
from .specialists import specialists
from .managers import managers
routers = (
    cameras,
    specialists,
    managers,
)

def include_routers(app: FastAPI) -> None:
    for router in routers:
        app.include_router(router)

    app.include_router(
        fastapi_users.get_auth_router(auth_backend),
        prefix="/auth/jwt",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_users_router(
            UserRead, 
            UserUpdate, 
            requires_verification=True
        ),
        prefix="/users",
        tags=["users"],
    )