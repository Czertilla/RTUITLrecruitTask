from database.models.cases import CaseORM
from database.engine import new_session
from schemas.cameras import SCaseInsert
from datetime import datetime, UTC, timezone


class CaseRepo:
    @classmethod
    async def insert(cls, data: SCaseInsert):
        record = data.model_dump()
        async with new_session() as session:
            session.add(CaseORM(**record))
            await session.flush()
            await session.commit()
