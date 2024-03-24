from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from api.dependencies import get_camera_service, get_case_service
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
    service: Annotated[CameraService, Depends(get_camera_service)]
) -> UUID:
    return await service.regist(request)

@cameras.post("/case")
async def send_case(
    request: Annotated[SCameraCase, Depends()],
    case_service: Annotated[CaseService, Depends(get_case_service)],
) -> None:
    answer = await case_service.handle_case(request)
    if answer is not None:
        raise HTTPException(status_code=422, detail=jsonable_encoder(answer))
