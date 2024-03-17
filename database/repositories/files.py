from database.models.files import FileORM
from database.engine import new_session
from database.models.files import FileORM


class FileRepo():
    @classmethod
    async def insert(cls, data: bytes):
        async with new_session() as session:
            session.add(file:=FileORM(data=data))
            await session.flush()
            await session.commit()
        return file.ID