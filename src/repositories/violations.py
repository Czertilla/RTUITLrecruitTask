from models import ViolationORM
from .export import ExportRepo

class ViolationRepo(ExportRepo):
    model = ViolationORM

    async def export(self, data: list[dict]) -> dict:
        return await super().export(data, "violation_type")
