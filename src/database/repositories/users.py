from typing import AsyncGenerator
from uuid import UUID
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from fastapi import Depends
from database.engine import new_session
from logging import getLogger

from database.models.users import UserORM

logger = getLogger(__name__)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, UserORM)

class UserRepo:
    @classmethod
    async def merge(cls, model: UserORM):
        async with new_session() as session:
            await session.merge(model)
            await session.flush()
            await session.commit()

    @classmethod 
    async def check_username(cls, value) -> bool:
        async with new_session() as session:
            user = (
                await session.execute(
                    select(UserORM).
                    where(UserORM.username == value)
                )
            ).scalar_one_or_none()
        return user is not None

    @classmethod
    async def find_by_id(cls, id: UUID) -> UserORM|None:
        stmt = select(UserORM).where(UserORM.id == id)
        async with new_session() as session:
            result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def verify(cls, id: UUID) -> UserORM|None:
        user = await cls.find_by_id(id)
        if user is None:
            logger.error("user %s not found", id)
            logger.warning("%s user not verified", id)
            return
        user.is_verified = True
        user.role = "specialist"
        await cls.merge(user)
        return user
    
    @classmethod
    async def set_manager(cls, id: UUID):
        user = await cls.find_by_id(id)
        if user is None:
            logger.error("user %s not found", id)
            logger.warning("superuser status for user %s is not set", id)
            return
        user.is_superuser = True
        user.is_active = True
        user.is_verified = True
        user.role = "manager"
        await cls.merge(user)