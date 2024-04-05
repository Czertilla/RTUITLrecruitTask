from uuid import UUID

from models.votes import VoteORM
from sqlalchemy import delete, select, update
from database import BaseRepo

class VoteRepo(BaseRepo):
    model = VoteORM

    async def set_vote(
        self, 
        case_id: UUID, 
        user_id: UUID, 
        justify: bool
    ):
        stmt = (
            update(self.model).
            where(
                self.model.case_id == case_id,
                self.model.user_id == user_id
            ).
            values(
                justify=justify
            )
        )
        await self.execute(stmt)


    async def slice(self, case_id: UUID, count: int, skill: int):
        stmt = (
            select(self.model).
            where(
                self.model.case_id == case_id,
                self.model.skill == skill
            ).
            order_by(self.model.timestamp)
        )
        votes_list: list[self.model] = (await self.execute(stmt)).scalars().all()
        target_list = [vote.id for vote in votes_list][count:]
        stmt = (
            delete(self.model).
            where(self.model.id in target_list)
        )
        await self.execute(stmt)

