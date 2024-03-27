from models import CarOwnerORM
from .export import ExportRepo

class CarOwnerRepo(ExportRepo):
    model = CarOwnerORM

    async def export(self, data: list[dict]) -> dict:
        return await super().export(data, "car_number")
