from typing import Any
from uuid import uuid4, UUID
from sqlalchemy.types import JSON, DateTime
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.declarative import declared_attr
from uuid import UUID
from sqlalchemy import Result, insert, select
from database import new_session
from utils.abstract_repo import AbstractRepository

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

    async def execute(self, stmt, flush=True, commit=True) -> Result:
        async with new_session() as session:
            result: Result = await session.execute(statement=stmt)
            if flush:
                await session.flush()
            if commit:
                await session.commit()
        return result


    async def add_one(self, data: dict) -> UUID:
        stmt = (
            insert(self.model).
            values(**data).
            returning(self.model.id)
        )
        return (await self.execute(stmt, flush=False)).scalar_one()
    
    async def find_by_id(self, id: UUID) -> model: # type: ignore
        stmt = (
            select(self.model).
            where(self.model.id == id)
        )
        return (await self.execute(stmt, flush=False, commit=False)).scalar_one()

    async def find_all(self) -> list[model]: # type: ignore
        stmt = select(self.model)
        result = await self.execute(stmt)
        result = [row[0].to_read_model() for row in result.all()]
        return result