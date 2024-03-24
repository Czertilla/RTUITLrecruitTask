from typing import Any
from uuid import uuid4, UUID
from sqlalchemy.types import JSON, DateTime
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.asyncio.session import AsyncSession
from uuid import UUID
from sqlalchemy import Result, insert, select
from utils.absract.repository import AbstractRepository
 
class IdMinxin:
    @declared_attr
    def id(cls) -> Mapped[UUID]:
        return mapped_column(primary_key=True, default=uuid4)

class Base(DeclarativeBase, IdMinxin):
    __abstract__ = True
    
    type_annotation_map = {
        dict[str, Any]: JSON,
        datetime: DateTime(timezone=True)
    }

class SQLAlchemyRepository(AbstractRepository):
    model = Base

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session = session

    async def execute(self, stmt, flush=False) -> Result:
        result: Result = await self.session.execute(statement=stmt)
        if flush:
            await self.session.flush()
        return result

    async def merge(self, data_orm: model, flush=False):
        await self.session.merge(data_orm)
        if flush:
            await self.session.flush()


    async def add_one(self, data: dict) -> UUID:
        stmt = (
            insert(self.model).
            values(**data).
            returning(self.model.id)
        )
        return (await self.execute(stmt, flush=False)).scalar_one()
    

    async def find_by_id(self, id: UUID) -> model:
        stmt = (
            select(self.model).
            where(self.model.id == id)
        )
        return (await self.execute(stmt)).scalar_one_or_none()


    async def find_all(self) -> list[model]:
        stmt = select(self.model)
        result = await self.execute(stmt)
        result = [row[0].to_read_model() for row in result.all()]
        return result
    

    async def check_existence(self, id: UUID) -> bool:
        return (await self.find_by_id(id)) is not None
