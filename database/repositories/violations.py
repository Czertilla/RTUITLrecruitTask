from pandas import DataFrame
from database.engine import new_session
from typing import Type
from database.models.base import Base
from database.models import ViolationORM
from .export import ExportRepo

class ViolationRepo(ExportRepo):
    orm = ViolationORM

    @classmethod
    async def export(cls, data: list[dict]) -> dict:
        return await super().export(data, "violation_type")
