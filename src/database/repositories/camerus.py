from sqlalchemy import select, update
from ..engine import new_session
from ..models.camerus import DependenciesOrm
from uuid import UUID
import logging
from utils.exceptor import Exceptor

logger = logging.getLogger(__name__)
exc = Exceptor()

class CamerusRepo():
    @classmethod
    @exc.aiotect
    async def insert(cls, data: DependenciesOrm) -> UUID:
        async with new_session() as session:
            session.add(data)
            await session.flush()
            await session.commit()
        return data.id


    @classmethod
    @exc.aiotect
    async def create_root(cls, root_name: str) -> UUID|None:
        async with new_session() as session:
            if (
                await session.execute(
                    select(DependenciesOrm.id).
                    where(DependenciesOrm.key == root_name))
            ).all():
                logger.error("%s Camerus dataType already exist", root_name)
                raise TypeError
        
        dependency = DependenciesOrm(
            key = root_name,
            value_type = "dict"
        )
        return await cls.insert(dependency)

    @classmethod
    @exc.aiotect
    async def find_by_id(cls, id: UUID) -> DependenciesOrm:
        async with new_session() as session:
            result: DependenciesOrm = (
                await session.execute(
                    select(DependenciesOrm).
                    where(DependenciesOrm.id == id)
                )
            ).scalar_one()
        return result

    @classmethod
    @exc.aiotect
    async def find_by_path(cls, path: str) -> UUID|None:
        async with new_session() as session:
            targetID = None
            for point in path.split('.'):
                targetID: DependenciesOrm = (
                    await session.execute(
                        select(DependenciesOrm.id).
                        where(
                            DependenciesOrm.key == point,
                            DependenciesOrm.enclosure == targetID
                        )
                    )
                ).scalar()
            return targetID


    @classmethod
    @exc.aiotect
    async def put(cls, path: str, name: str, value_type: str, destination: str = None, field_attrs: dict = {}) -> UUID:
        dependency = DependenciesOrm(
            key = name,
            value_type = value_type,
            destination = destination,
            field_attrs = field_attrs
        )
        DependenciesOrm()
        targetID = await cls.find_by_path(path)
        if targetID is None:
            raise NameError
        dependency.enclosure = targetID
        async with new_session() as session:
            if result:=(await session.execute(
                select(DependenciesOrm.id).
                where(DependenciesOrm.key == dependency.key,
                      DependenciesOrm.enclosure == dependency.enclosure)
            )).scalar():
                await session.execute(
                        update(DependenciesOrm).                                                                                                   
                        where(DependenciesOrm.id == result).
                        values(
                            field_attrs = dependency.field_attrs,
                            value_type = dependency.value_type,
                            destination = dependency.destination
                        ))
                await session.flush()
                await session.commit()
            else:
                result = await cls.insert(dependency)
        return result
        


    @classmethod
    @exc.aiotect
    async def get(cls, path: str|UUID) -> DependenciesOrm:
        if type(path) == UUID:
            targetID = path
        else:
            targetID = await cls.find_by_path(path)
        async with new_session() as session:
            return (await session.execute(
                select(DependenciesOrm).where(DependenciesOrm.id == targetID)
            )).one()


    @classmethod
    @exc.aiotect
    async def construct(cls, dictID: UUID) -> list[DependenciesOrm]:
        dependency: DependenciesOrm = await cls.find_by_id(dictID)
        if  dependency.value_type != "dict":
            raise TypeError
        async with new_session() as session:
            dependencies = (await
                session.execute(
                    select(DependenciesOrm).
                    where(DependenciesOrm.enclosure == dictID)
                )
            ).scalars().all()
        return dependencies
        

    
    @classmethod
    @exc.aiotect
    async def collect(cls) -> tuple[UUID]:
        stmt = select(DependenciesOrm.id).where(DependenciesOrm.enclosure == None)
        async with new_session() as session:
            result = await session.execute(stmt)
        return result.scalars().all()
