from sqlalchemy.ext.asyncio import async_sessionmaker
from app.config import Settings

match (settings:=Settings()).DB_DBMS:
    case "sqlite":
        from .sqlite import engine
    case "postgres":
        from .pgsql import engine

new_session = async_sessionmaker(engine, expire_on_commit=False)
