from uuid import UUID
from repositories.camerus import CamerusRepo
from repositories.files import FileRepo
from schemas.cameras import SCameraCase, SCaseInsert
from services.dynamic import CamerusService
from services.files import FileService
from utils.abstract_repo import AbstractRepository
from utils.abstract_serv import BaseService
from utils.requests import deserialize


class CaseService(BaseService):
    def __init__(self, repository: AbstractRepository) -> None:
        super().__init__(repository)
        self.camerus_service = CamerusService(CamerusRepo)
        self.file_service = FileService(FileRepo)

    
    async def insert(self, data: SCaseInsert) -> UUID:
        record = data.model_dump()
        return await self.repository.add_one(record)
    

    async def handle_case(
        self,
        case_schema: SCameraCase
    ) -> None:
        metadata = await deserialize(await case_schema.metadata.read())
        model, mdl_name = await self.camerus_service.validate(metadata)
        if type(model) is dict:
            return model
        byte_array = await case_schema.photo.read()
        case_data = (await self.camerus_service.parse(model, mdl_name))
        case_data.update(
            {"photo_id": await self.file_service.upload_bytes(byte_array)}
        )
        model = SCaseInsert.model_validate(case_data)
        await self.insert(model)


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
