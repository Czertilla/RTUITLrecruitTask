from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas.cameras import SCameraRegist, SCameraCase
from schemas.dynamic import DynamicModels
from database.repositories import CameraRepo
from uuid import UUID
from pydantic import ValidationError
from utils.requests import deserialize
from logging import getLogger

logger = getLogger(__name__)

cameras = APIRouter(prefix="/cameras")

@cameras.post("/regist")
async def regist(request: SCameraRegist) -> UUID:
    return (await CameraRepo.regist(
        latitude=request.GPScoords.latitude,
        longitude=request.GPScoords.longitude,
        description=request.description,
        cam_type=request.CameraType
    ))

@cameras.post("/case")
async def send_case(request: SCameraCase) -> None:
    metadata = await deserialize(request.metadata)
    model = await DynamicModels.validate(metadata)
    if type(model) is dict:
        raise HTTPException(status_code=422, detail=jsonable_encoder(model))
    
    
