from uuid import UUID

from fastapi import UploadFile
from models.files import FileORM
from utils.abstract_serv import BaseService


class FileService(BaseService):
    async def upload_bytes(self, data: bytes) -> UUID:
        file_data = {"data": data}
        return await self.repository.add_one(file_data)
    

    async def download_bytes(self, file_id: UUID) -> bytes|None:
        file_orm: FileORM = await self.repository.find_by_id(file_id)
        return file_orm.data
