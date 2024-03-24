from sqlalchemy import select, update
from database import new_session
from models.camerus import DependenciesOrm
from uuid import UUID
from database import BaseRepo
import logging

logger = logging.getLogger(__name__)

class CamerusRepo(BaseRepo):
    model = DependenciesOrm

    async def insert(self, data: model) -> UUID:
        return self.add_one(data)


    async def create_root(self, root_name: str) -> UUID|None:
        async with new_session() as session:
            if (
                await session.execute(
                    select(self.model.id).
                    where(self.model.key == root_name))
            ).all():
                logger.error("%s Camerus dataType already exist", root_name)
                raise TypeError
        
        dependency = self.model(
            key = root_name,
            value_type = "dict"
        )
        return await self.insert(dependency)


    async def find_by_id(self, id: UUID) -> model:
        async with new_session() as session:
            result: self.model = (
                await session.execute(
                    select(self.model).
                    where(self.model.id == id)
                )
            ).scalar_one()
        return result


    async def find_by_path(self, path: str) -> UUID|None:
        async with new_session() as session:
            targetID = None
            for point in path.split('.'):
                targetID: self.model = (
                    await session.execute(
                        select(self.model.id).
                        where(
                            self.model.key == point,
                            self.model.enclosure == targetID
                        )
                    )
                ).scalar()
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
        async with new_session() as session:
            if result:=(await session.execute(
                select(self.model.id).
                where(self.model.key == dependency.key,
                      self.model.enclosure == dependency.enclosure)
            )).scalar():
                await session.execute(
                        update(self.model).                                                                                                   
                        where(self.model.id == result).
                        values(
                            field_attrs = dependency.field_attrs,
                            value_type = dependency.value_type,
                            destination = dependency.destination
                        ))
                await session.flush()
                await session.commit()
            else:
                result = await self.insert(dependency)
        return result
        

    async def get(self, path: str|UUID) -> model:
        if type(path) == UUID:
            targetID = path
        else:
            targetID = await self.find_by_path(path)
        async with new_session() as session:
            return (await session.execute(
                select(self.model).where(self.model.id == targetID)
            )).one()


    async def construct(self, dictID: UUID) -> list[model]:
        dependency = await self.find_by_id(dictID)
        if  dependency.value_type != "dict":
            raise TypeError
        async with new_session() as session:
            dependencies = (await
                session.execute(
                    select(self.model).
                    where(self.model.enclosure == dictID)
                )
            ).scalars().all()
        return dependencies


    async def collect(self) -> tuple[UUID]:
        stmt = select(self.model.id).where(self.model.enclosure == None)
        async with new_session() as session:
            result = await session.execute(stmt)
        return result.scalars().all()
