from uuid import UUID
from models.cases import CaseORM, CaseStatus
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database import BaseRepo

class CaseRepo(BaseRepo):
    model = CaseORM


    async def find_new_for_vote(self, skill: int, user_id: UUID) -> list[model]:
        stmt = (
            select(self.model).
            where(
                self.model.skill_value == skill,
                self.model.status == CaseStatus.INITIATED
            ).
            # options(
            #     selectinload(self.model.users_list)
            # ).
            filter_by(
                all(
                    self.model.users_list, 
                    lambda x: x.id != user_id
                )
            )
        )
        return (await self.execute(stmt)).scalars().all()


    # async def vote(self, user: UserORM, vote: str) -> str:
    #     if (case_data := await self.get_current_case(user)) is None:
    #         return "case not selected"
    #     return "OK"

        
        