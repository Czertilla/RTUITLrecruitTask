from uuid import UUID
from schemas.cameras import SCameraCase, SCaseInsert
from services.dynamic import CamerusService
from units_of_work.case import CaseUOW
from utils.absract.service import BaseService
from utils.requests import deserialize


class CaseService(BaseService):
    async def handle_case(
        self,
        case_schema: SCameraCase
    ) -> None:
        metadata = await deserialize(await case_schema.metadata.read())
        model, mdl_name = await (camerus_service:= CamerusService(self.uow)).validate(metadata)
        if type(model) is dict:
            return model
        byte_array = await case_schema.photo.read()
        case_data = (await camerus_service.parse(model, mdl_name))
        async with self.uow:
            case_data.update(
                {"photo_id": await self.uow.files.upload_bytes(byte_array)}
            )
            model = SCaseInsert.model_validate(case_data).model_dump()
            result = await self.uow.cases.add_one(model)
            await self.uow.commit()
        return result
        


    # async def get_current_case(self, user: UserORM) -> CaseORM|None:
    #     for vote in user.votes_list:
    #         if vote.justify is None:
    #             return vote.case_model

    # @classmethod
    # async def get_random_case(self, user: UserORM) -> CaseORM|None:
    #     async with new_session() as session:
    #         user = await session.scalar(
    #             select(UserORM). 
    #             where(UserORM.id == user.id).
    #             options(selectinload(UserORM.votes_list), selectinload(UserORM.cases_list))
    #         )
    #     if (case_data:= await self.get_current_case(user)) is None:
    #         stmt = (
    #             select(CaseORM).
    #             where(
    #                 CaseORM.skill_value == user.skill
    #             ).
    #             options(selectinload(CaseORM.votes_list), selectinload(CaseORM.users_list))
    #         )
    #     else:
    #         return case_data
    #     async with new_session() as session:
    #         result = await session.execute(stmt)
    #     cases_list:list = result.scalars().all()
    #     while len(cases_list) > 0:
    #         case_data: CaseORM = cases_list.pop(randint(0, len(cases_list)-1))
    #         if user not in case_data.users_list:
    #             user.cases_list.append(case_data)
    #             UserRepo.merge(user)
    #             return case_data

    # @classmethod
    # async def vote(self, user: UserORM, vote: str) -> str:
    #     if (case_data := await self.get_current_case(user)) is None:
    #         return "case not selected"
    #     return "OK"
