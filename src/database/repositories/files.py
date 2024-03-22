from uuid import UUID

from sqlalchemy import select
from database.models.files import FileORM
from database.engine import new_session
from database.models.files import FileORM


class FileRepo():
    @classmethod
    async def insert(cls, data: bytes) -> UUID:
        async with new_session() as session:
            session.add(file:=FileORM(data=data))
            await session.flush()
            await session.commit()
        return file.id
    
    @classmethod
    async def download_bytes(cls, request_id: UUID) -> bytes|None:
        stmt = select(FileORM.data).where(FileORM.id == request_id)
        async with new_session() as session:
            result = await session.execute(stmt)
        return result.scalar_one_or_none()