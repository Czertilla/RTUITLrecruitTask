from models import CarOwnerORM
from .export import ExportRepo

class CarOwnerRepo(ExportRepo):
    orm = CarOwnerORM

    @classmethod
    async def export(cls, data: list[dict]) -> dict:
        return await super().export(data, "car_number")
