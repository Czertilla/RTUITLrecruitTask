from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas.cameras import SCameraRegist, SCameraCase
from schemas.dynamic import DynamicModels
from uuid import UUID, uuid4
from pydantic import ValidationError
from utils.requests import deserialize
from logging import getLogger

logger = getLogger(__name__)

cameras = APIRouter(prefix="/cameras")

@cameras.post("/regist")
def regist(request: SCameraRegist) -> UUID:
    return uuid4()

@cameras.post("/case")
async def send_case(request: SCameraCase) -> None:
    metadata = await deserialize(request.metadata)
    model = await DynamicModels.validate(metadata)
    if type(model) is dict:
        raise HTTPException(status_code=422, detail=jsonable_encoder(model))
    print(model)
    
    
