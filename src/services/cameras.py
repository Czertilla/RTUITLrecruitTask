from uuid import UUID

from utils.abstract_serv import BaseService
from schemas.cameras import SCameraRegist

class CameraService(BaseService):
    async def regist(
        self, 
        camera_schema: SCameraRegist
    ) -> UUID:
        camera_data = camera_schema.model_dump()
        camera_data.update(camera_data.pop("GPScoords"))
        camera_data.update({
            "cam_type": await self.repository.find_by_path(
                camera_data.pop("CameraType")
            )
        })
        return await self.repository.add_one(camera_data)
