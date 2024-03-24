from logging import getLogger
from uuid import UUID
from models.users import UserORM
from schemas.cameras import SCameraCase, SCaseInsert
from utils.absract.service import BaseService
from utils.requests import deserialize

logger = getLogger(__name__)

class UserService(BaseService):
    async def check_username(self, value: str) -> bool:
        async with self.uow:
            self.uow.users.check_username(value)


    async def verify(self, id: UUID) -> UserORM|None:
        async with self.uow:
            user: UserORM = await self.uow.users.find_by_id(id)
            if user is None:
                logger.error("user %s not found", id)
                logger.warning("%s user not verified", id)
                return
            user.is_verified = True
            user.role = "specialist"
            await self.uow.users.merge(user)
            await self.uow.commit()
            return user
    

    async def set_manager(self, id: UUID):
        async with self.uow:
            user: UserORM = await self.uow.users.find_by_id(id)
            if user is None:
                logger.error("user %s not found", id)
                logger.warning("superuser status for user %s is not set", id)
                return
            user.is_superuser = True
            user.is_active = True
            user.is_verified = True
            user.role = "manager"
            await self.uow.users.merge(user)
            await self.uow.commit()