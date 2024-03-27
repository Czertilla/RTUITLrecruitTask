from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response

from api.auth.auth import fastapi_users
from api.dependencies import SpecialistUOWDep
from models.users import UserORM
from repositories.cases import CaseRepo
from repositories.files import FileRepo
from schemas.specialists import SGetCaseResponse, SVoteRequest, SVoteResponce, SCaseGet
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
    uow: SpecialistUOWDep):
    response = await CaseService(uow).get_random_case(user)
    if response is None:
        raise HTTPException(status_code=404, detail="Case with appropriate skill value not found")
    return Response(content=response.photo, media_type="image/png")

@specialists.post("/vote")
async def vote(
    vote: SVoteRequest, 
    uow: SpecialistUOWDep,
    user: UserORM = Depends(specialist)
) -> SVoteResponce:
    service = CaseService(uow)
    if type(status:= await service.vote(user, vote.vote == "justify")) == UUID:
        status = "OK"
    return {
        "status": status
    }