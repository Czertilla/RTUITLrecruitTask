from uuid import UUID
from sqlalchemy import select
from database.engine import new_session
from database.models import ViolationORM
from .export import ExportRepo

class ViolationRepo(ExportRepo):
    orm = ViolationORM

    @classmethod
    async def export(cls, data: list[dict]) -> dict:
        return await super().export(data, "violation_type")

    @classmethod
    async def find_by_id(cls, id: UUID) -> ViolationORM:
        async with new_session() as session:
            violation = (
                await session.execute(
                    select(ViolationORM).
                    where(ViolationORM.id == id)
                )
            ).scalar_one_or_none()
        return violation

    @classmethod
    async def check_existence(cls, id: UUID) -> bool:
        return (await cls.find_by_id(id)) is not None