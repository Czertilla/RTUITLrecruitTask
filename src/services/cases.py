from uuid import UUID
from models.cases import CaseORM
from models.users import UserORM
from schemas.cameras import SCameraCase, SCaseInsert
from services.dynamic import CamerusService
from utils.absract.service import BaseService
from utils.requests import deserialize
from random import choice


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
        


    async def get_current_case(self, user: UserORM) -> CaseORM|None:
        for vote in user.votes_list:
            if vote.justify is None:
                return vote.case_model


    async def get_random_case(self, user: UserORM) -> CaseORM|None:
        async with self.uow:
            user = await self.uow.users.get(user.id)
            if (case_data:= await self.get_current_case(user)) is None:
                cases_list = await self.uow.cases.find_new_for_vote(user)
            else:
                return case_data
            case_model: CaseORM = choice(cases_list)
            case_model.users_list.append(user)
            await self.uow.cases.merge(case_model, flush=True)
        return case_model


    async def vote(self, user: UserORM, vote: str) -> str:
        if (case_data := await self.get_current_case(user)) is None:
            return "case not selected"
        return "OK"
