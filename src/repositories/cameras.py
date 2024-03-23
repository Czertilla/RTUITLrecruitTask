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

    async def regist(
        self, 
        latitude: float, 
        longitude: float,
        description: str,
        cam_type: str
    ) -> UUID:
        cam_type_id = await CamerusRepo.find_by_path(cam_type)
        camera = CameraOrm(
            latitude=latitude, 
            longitude=longitude, 
            description=description, 
            cam_type=cam_type_id
        )
        return await self.insert(camera)


    @classmethod
    async def insert(self, camera: CameraOrm) -> UUID:
        async with new_session() as session:
            session.add(camera)
            await session.flush()
            await session.commit()
        return camera.id

    @classmethod
    async def find_by_id(self, id: UUID) -> CameraOrm:
        async with new_session() as session:
            camera = (await session.execute(
                select(CameraOrm).
                where(CameraOrm.id == id)
            )).scalar_one_or_none()
            camera.cam_type = (await CamerusRepo.find_by_id(camera.cam_type)).key
        return camera

    @classmethod
    async def check_existence(self, id: UUID) -> bool:
        return (await self.find_by_id(id)) is not None