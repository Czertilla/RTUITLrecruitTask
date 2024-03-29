import uuid
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from app.auth.core import get_user_manager
from database.engine import settings
from fastapi_users import FastAPIUsers
from database.models.users import UserORM


SECRET = settings.USERS_SECTRET
cookie_transport = CookieTransport(cookie_name="auth", cookie_max_age=3600)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[UserORM, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
