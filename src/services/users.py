from uuid import UUID
from schemas.cameras import SCameraCase, SCaseInsert
from utils.requests import deserialize


class Userservice:
    ...
    # @classmethod 
    # async def check_username(self, value) -> bool:
    #     stmt = (
    #         select(UserORM).
    #         where(UserORM.username == value)
    #     )
    #         ).scalar_one_or_none()
    #     return user is not None

    # @classmethod
    # async def find_by_id(self, id: UUID) -> UserORM|None:
    #     stmt = select(UserORM).where(UserORM.id == id)
    #     async with new_session() as session:
    #         result = await session.execute(stmt)
    #     return result.scalar_one_or_none()

    # @classmethod
    # async def verify(self, id: UUID) -> UserORM|None:
    #     user = await self.find_by_id(id)
    #     if user is None:
    #         logger.error("user %s not found", id)
    #         logger.warning("%s user not verified", id)
    #         return
    #     user.is_verified = True
    #     user.role = "specialist"
    #     await self.merge(user)
    #     return user
    
    # @classmethod
    # async def set_manager(self, id: UUID):
    #     user = await self.find_by_id(id)
    #     if user is None:
    #         logger.error("user %s not found", id)
    #         logger.warning("superuser status for user %s is not set", id)
    #         return
    #     user.is_superuser = True
    #     user.is_active = True
    #     user.is_verified = True
    #     user.role = "manager"
    #     await self.merge(user)