from fastapi import APIRouter
from schemas.cameras import SCameraRegist, BaseCamerus
from uuid import UUID, uuid4

cameras = APIRouter(prefix="/cameras")

@cameras.get("")
async def check():
    return "FINE"