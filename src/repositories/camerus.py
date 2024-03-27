from sqlalchemy import select, update
from models.camerus import DependenciesOrm
from uuid import UUID
from database import BaseRepo
import logging

logger = logging.getLogger(__name__)

class CamerusRepo(BaseRepo):
    model = DependenciesOrm

    async def create_root(self, root_name: str) -> UUID|None:
        stmt = (
            select(self.model.id).
            where(self.model.key == root_name)
        )
        if (await self.execute(stmt)).all():
            logger.error("%s Camerus dataType already exist", root_name)
            return
        
        dependency = self.model(
            key = root_name,
            value_type = "dict"
        )
        return await self.merge(dependency)


    async def find_by_path(self, path: str) -> UUID|None:
        targetID = None
        for point in path.split('.'):
            stmt = (
                select(self.model.id).
                where(
                    self.model.key == point,
                    self.model.enclosure == targetID
                )
            )
            targetID: self.model = (await self.execute(stmt)).scalar_one_or_none()
        return targetID


    async def put(
        self, 
        path: str, 
        name: str, 
        value_type: str, 
        destination: str = None, 
        field_attrs: dict = {}
    ) -> UUID:
        dependency = self.model(
            key = name,
            value_type = value_type,
            destination = destination,
            field_attrs = field_attrs
        )
        targetID = await self.find_by_path(path)
        if targetID is None:
            raise NameError
        dependency.enclosure = targetID
        stmt = (
            select(self.model.id).
            where(
                self.model.key == dependency.key,
                self.model.enclosure == dependency.enclosure
            )
        )
        if result:=(await self.execute(stmt)).scalar_one_or_none():
            stmt = (
                update(self.model).                                                                                                   
                where(self.model.id == result).
                values(
                    field_attrs = dependency.field_attrs,
                    value_type = dependency.value_type,
                    destination = dependency.destination
                )
            )
            await self.execute(stmt, flush=True)
        else:
            result = await self.merge(dependency)
        return result
        

    async def get(self, path: str|UUID) -> model:
        if type(path) == UUID:
            targetID = path
        else:
            targetID = await self.find_by_path(path)
        return await self.find_by_id(targetID)


    async def construct(self, dictID: UUID) -> list[model]:
        dependency = await self.find_by_id(dictID)
        if  dependency.value_type != "dict":
            raise TypeError
        dependencies = (await self.find_all(enclosure=dictID))
        return dependencies


    async def collect(self) -> tuple[UUID]:
        stmt = select(self.model.id).where(self.model.enclosure == None)
        result = await self.execute(stmt)
        return result.scalars().all()
