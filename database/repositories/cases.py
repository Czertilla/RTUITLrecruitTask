from typing import TYPE_CHECKING
from database.models.cases import CaseORM
from database.engine import new_session
from schemas.cameras import SCaseInsert
from sqlalchemy import select
from database.models import UserORM


class CaseRepo:
    @classmethod
    async def insert(cls, data: SCaseInsert):
        record = data.model_dump()
        async with new_session() as session:
            session.add(CaseORM(**record))
            await session.flush()
            await session.commit()
    
    @classmethod
    async def get_current_case(cls, user: UserORM) -> CaseORM|None:
        for vote in user.case_associations:
            if vote.justify is None:
                return vote.case_table

    @classmethod
    async def get_random_case(cls, user: UserORM) -> CaseORM|None:
        if (case_data:= await cls.get_current_case(user)) is None:
            stmt = (
                select(CaseORM).
                where(
                    CaseORM.skill_value == user.skill,
                    user not in CaseORM.users
                )
            )
        else:
            return case_data
        user.cases.append(case_data)
        async with new_session() as session:
            result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def vote(cls, user: UserORM, vote: str) -> str:
        if (case_data := await cls.get_current_case(user)) is None:
            return "case not selected"

        
        