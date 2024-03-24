from typing import AsyncGenerator
from uuid import UUID
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from fastapi import Depends
from database import new_session, BaseRepo
from logging import getLogger

from models.users import UserORM

logger = getLogger(__name__)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, UserORM)

class UserRepo(BaseRepo):
    async def merge(cls, model: UserORM):
        async with new_session() as session:
            await session.merge(model)
            await session.flush()
            await session.commit()


    async def check_username(cls, value) -> bool:
        async with new_session() as session:
            user = (
                await session.execute(
                    select(UserORM).
                    where(UserORM.username == value)
                )
            ).scalar_one_or_none()
        return user is not None

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

