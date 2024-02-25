from fastapi import APIRouter
from schemas.cameras import SCameraRegist, camerus1
from uuid import UUID, uuid4

cameras = APIRouter(prefix="/cameras")

@cameras.post("/regist")
def regist(request: SCameraRegist) -> UUID:
    return uuid4()

