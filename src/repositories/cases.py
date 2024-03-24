from typing import TYPE_CHECKING
from models.cases import CaseORM
from database import new_session
from models.votes import VoteORM
from repositories.users import UserRepo
from schemas.cameras import SCaseInsert
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models import UserORM
from random import randint
from database import BaseRepo

class CaseRepo(BaseRepo):
    async def get_current_case(self, user: UserORM) -> CaseORM|None:
        for vote in user.votes_list:
            if vote.justify is None:
                return vote.case_model


    async def get_random_case(self, user: UserORM) -> CaseORM|None:
        async with new_session() as session:
            user = await session.scalar(
                select(UserORM). 
                where(UserORM.id == user.id).
                options(selectinload(UserORM.votes_list), selectinload(UserORM.cases_list))
            )
        if (case_data:= await self.get_current_case(user)) is None:
            stmt = (
                select(CaseORM).
                where(
                    CaseORM.skill_value == user.skill
                ).
                options(selectinload(CaseORM.votes_list), selectinload(CaseORM.users_list))
            )
        else:
            return case_data
        async with new_session() as session:
            result = await session.execute(stmt)
        cases_list:list = result.scalars().all()
        while len(cases_list) > 0:
            case_data: CaseORM = cases_list.pop(randint(0, len(cases_list)-1))
            if user not in case_data.users_list:
                user.cases_list.append(case_data)
                UserRepo.merge(user)
                return case_data


    async def vote(self, user: UserORM, vote: str) -> str:
        if (case_data := await self.get_current_case(user)) is None:
            return "case not selected"
        return "OK"

        
        