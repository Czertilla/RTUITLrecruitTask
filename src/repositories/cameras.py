from sqlalchemy import select, exists

from database import BaseRepo
from repositories.camerus import CamerusRepo

from database import new_session
from models.cameras import CameraOrm
from uuid import UUID
import logging
from utils.exceptor import Exceptor

logger = logging.getLogger(__name__)
exc = Exceptor()

class CameraRepo(BaseRepo):
    model = CameraOrm


    async def check_existence(self, id: UUID) -> bool:
        return (await self.find_by_id(id)) is not None
    

    async def find_by_path(self, camerus_name: str)-> UUID:
        return await CamerusRepo().find_by_path(camerus_name)