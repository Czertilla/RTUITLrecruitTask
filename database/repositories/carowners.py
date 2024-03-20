from pandas import DataFrame
from database.engine import new_session
from typing import Type
from database.models.base import Base
from database.models import CarOwnerORM
from .export import ExportRepo

class CarOwnerRepo(ExportRepo):
    orm = CarOwnerORM

    @classmethod
    async def export(cls, data: list[dict]) -> dict:
        return await super().export(data, "car_number")
