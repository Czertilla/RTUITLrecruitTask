from uuid import UUID
from models.cases import CaseORM
from models.users import UserORM
from models.votes import VoteORM
from schemas.cameras import SCameraCase, SCaseInsert
from schemas.specialists import SCaseGet, SGetCaseResponse
from services.dynamic import CamerusService
from utils.absract.service import BaseService
from utils.requests import deserialize
from secrets import choice


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
            # print(case_data.get("photo_id"))
            model = SCaseInsert.model_validate(case_data).model_dump()
            result = await self.uow.cases.add_one(model)
            await self.uow.commit()


    async def get_current_case(self, user: UserORM) -> CaseORM|None:
        for vote in user.votes_list:
            if vote.justify is None:
                return vote.case_model


    async def get_case_response(self, case_model: CaseORM) -> SGetCaseResponse:
        async with self.uow:
            photo = await self.uow.files.download_bytes(case_model.photo_id)
            violation = await self.uow.violations.find_by_id(case_model.violation_id)
            violation_type = getattr(violation, "violation_type", "unknow")
            violation_val = getattr(violation, "violation_value", "")
        return SGetCaseResponse(
            photo=photo,
            metadata=SCaseGet(
                transport=case_model.transport,
                violation_type=violation_type,
                case_timestamp=case_model.case_timestamp,
                violation_value=violation_val
            )
        )

    async def get_random_case(self, user: UserORM) -> SGetCaseResponse|None:
        async with self.uow:
            user = await self.uow.users.get(user.id)
            case_model = await self.get_current_case(user)
            if case_model is None:
                cases_list = await self.uow.cases.find_new_for_vote(
                    user.skill, [cm.id for cm in user.cases_list])
                if not cases_list:
                    return
                case_model: CaseORM = choice(cases_list)
                vote = VoteORM(case_id=case_model.id, user_id=user.id)
                case_model.votes_list.append(vote)
                await self.uow.cases.merge(case_model, flush=True)
            await self.uow.commit()
        return await self.get_case_response(case_model)


    async def vote(self, user: UserORM, justify: bool) -> str|UUID:
        async with self.uow:
            user = await self.uow.users.get(user.id)
            case_model = await self.get_current_case(user)
            if case_model is None:
                return "case not selected"
            await self.uow.cases.vote(case_model.id, user.id, justify)
            result = case_model.id
            await self.uow.commit()
        return result
