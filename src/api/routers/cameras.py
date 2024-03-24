from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from api.dependencies import CameraUOWDep, CaseUOWDep
from schemas.cameras import SCameraRegist, SCameraCase
from services.cameras import CameraService
from services.cases import CaseService
from uuid import UUID
from logging import getLogger

logger = getLogger(__name__)

cameras = APIRouter(prefix="/cameras", tags=["cams"])

@cameras.post("/regist")
async def regist(
    request: SCameraRegist, 
    uow: CameraUOWDep
) -> UUID:
    return await CameraService(uow).regist(request)

@cameras.post("/case")
async def send_case(
    request: Annotated[SCameraCase, Depends()],
    uow: CaseUOWDep,
) -> None:
    answer = await CaseService(uow).handle_case(request)
    if answer is not None:
        raise HTTPException(status_code=422, detail=jsonable_encoder(answer))
