from uuid import UUID
from models.cases import CaseORM, CaseStatus
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database import BaseRepo

class CaseRepo(BaseRepo):
    model = CaseORM


    async def find_new_for_vote(
        self, 
        skill: int, 
        users_cases_list: list[UUID]
    ) -> list[model]:
        stmt = (
            select(self.model).
            where(
                self.model.skill_value == skill,
                self.model.status == CaseStatus.INITIATED,
                self.model.id.not_in(users_cases_list),
            ).
            options(
                selectinload(self.model.users_list),
                selectinload(self.model.votes_list)
            )
        )
        return (await self.execute(stmt)).scalars().all()

    async def close(self, case_model: model):
        case_model.status = CaseStatus.EXTENDET
        await self.session.merge(case_model)
        