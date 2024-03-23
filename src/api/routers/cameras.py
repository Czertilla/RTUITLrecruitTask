from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas.cameras import Camerus, SCameraRegist, SCameraCase, SCaseInsert
from services.dynamic import DynamicModels
from repositories import CameraRepo, FileRepo
from uuid import UUID
from utils.requests import deserialize
from logging import getLogger
from repositories.cases import CaseRepo

logger = getLogger(__name__)

cameras = APIRouter(prefix="/cameras", tags=["cams"])

@cameras.post("/regist")
async def regist(request: SCameraRegist) -> UUID:
    return (await CameraRepo.regist(
        latitude=request.GPScoords.latitude,
        longitude=request.GPScoords.longitude,
        description=request.description,
        cam_type=request.CameraType
    ))

@cameras.post("/case")
async def send_case(request: SCameraCase = Depends()) -> None:
    metadata = await deserialize(await request.metadata.read())
    model, mdl_name = await DynamicModels.validate(metadata)
    if type(model) is dict:
        raise HTTPException(status_code=422, detail=jsonable_encoder(model))
    case_data = (await Camerus.parse(model, mdl_name))
    case_data.update(
        {"photo_id": await FileRepo.insert(await request.photo.read())}
    )
    model = SCaseInsert.model_validate(case_data)
    await CaseRepo.insert(model)
