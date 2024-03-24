from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, validator
from typing import Annotated, Type
from fastapi import Query, UploadFile

from repositories.camerus import CamerusRepo
from repositories.violations import ViolationRepo
from services.dynamic import CamerusService 
from repositories import CameraRepo
from asyncio import run


class SCoordsGPS(BaseModel):
    latitude: Annotated[float, Query(ge= -90, le=90, description="GPS latitude")]
    longitude: Annotated[float, Query(ge= -180, le=180, description="GPS longitude")]

class SCameraRegist(BaseModel):
    GPScoords: Annotated[SCoordsGPS, Query(title="GPS coordinates")]
    CameraType: Annotated[str, Query()]
    description: Annotated[str, Query(max_length=100)]

    @validator("CameraType")
    def check_camera_type(cls, value):
        if value not in (pattern:=CamerusService(CamerusRepo).camerus_pattern_list):
            raise ValueError(f"CameraType can be only {'|'.join(pattern)}")
        return value

class SCameraCase (BaseModel):
    photo: UploadFile
    metadata: UploadFile

class SCaseInsert (BaseModel):
    transport: Annotated[str, Field(pattern="[0-9][A-Z]{3}[0-9]{4}")]
    photo_id: UUID
    camera_id: UUID
    violation_id: UUID
    violation_value: Annotated[str, Field(max_length=100)]
    skill_value: Annotated[int, Field(ge=1, le=100)]
    case_timestamp: datetime
    class Config:
        from_atributes = True

    @validator("case_timestamp")
    def ensure_time_range(cls, value: datetime):
        if not value.timestamp() < datetime.now().timestamp():
            raise ValueError("the incident happened in the future")
        return value
    
    # @validator("camera_id")
    # async def check_camera_existence(cls, value: UUID):
    #     if not (await CameraRepo.check_existence(value)):
    #         raise ValueError(f"camera with id {value} doesn`t exist in database")

    # @validator("violation_id")
    # async def check_violation_existence(cls, value: UUID):
    #     if not  (await ViolationRepo.check_existence(value)):
    #         raise ValueError(f"violation with id {value} doesn`t exist in database")