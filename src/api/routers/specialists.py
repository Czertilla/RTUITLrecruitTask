from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response

from api.auth.auth import fastapi_users
from api.dependencies import UserUOWDep
from models.users import UserORM
from repositories.cases import CaseRepo
from repositories.files import FileRepo
from schemas.specialists import SGetCaseResponce, SVoteRequest, SVoteResponce, SCaseInsert
from services.cases import CaseService

specialist = fastapi_users.current_user(verified=True, superuser=False) 

specialists = APIRouter(prefix="/specs", tags=["specialists"])

@specialists.get(
        "/get-case",
        responses = {
            200: {
                "content": {"image/png": {}}
            }
        },
        response_class=Response
        )
async def get_case(
    user: Annotated[UserORM, Depends(specialist)],
    uow: UserUOWDep):
    if (case_data := await CaseService(uow).get_random_case(user)) is None:
        raise HTTPException(status_code=404, detail="Case with appropriate skill value not found")
    photo: bytes = await FileRepo.download_bytes(case_data.photo_id)
    metadata: SCaseInsert = SCaseInsert.model_validate(case_data.__dict__)
    return Response(content=photo, media_type="image/png")

@specialists.post("/vote")
async def vote(vote: SVoteRequest, user: UserORM = Depends(specialist)) -> SVoteResponce:
    status = await CaseRepo.vote(user, vote)
    return {
        "status": status
    }