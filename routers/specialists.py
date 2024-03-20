from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.auth.auth import fastapi_users
from database.models.users import UserORM
from database.repositories.cases import CaseRepo
from database.repositories.files import FileRepo
from schemas.specialists import SGetCaseResponce, SVoteRequest, SVoteResponce, SCaseInsert

specialist = fastapi_users.current_user(verified=True, superuser=False) 

specialists = APIRouter(prefix="/specs", tags=["specialists"])

@specialists.get("/get-case")
async def get_case(user: UserORM = Depends(specialist)) -> SGetCaseResponce:
    if (case_data := await CaseRepo.get_random_case(user)) is None:
        raise HTTPException(status_code=404, detail="Case with appropriate skill value not found")
    photo: bytes = await FileRepo.download_bytes(case_data.photo_id)
    metadata: SCaseInsert = SCaseInsert.model_validate(case_data)
    return {
        "photo": photo,
        "metadata": metadata
    }


@specialists.post("/vote")
async def vote(vote: SVoteRequest, user: UserORM = Depends(specialist)) -> SVoteResponce:
    status = await CaseRepo.vote(user, vote)
    return {
        "status": status
    }