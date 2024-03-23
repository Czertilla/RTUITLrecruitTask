from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, validator
from typing import Annotated, Type
from fastapi import Query, UploadFile

from database.repositories.violations import ViolationRepo
from src.services.dynamic import DynamicModels 
from database.repositories import CameraRepo
from asyncio import run

class Camerus:
    @classmethod
    def parse_camerus1(cls, data: dict) -> tuple:
        numbers = data.get("transport_numbers")
        return (
            f"{numbers[0]}{data.get('transport_chars')}{numbers[1:]}{data.get('transport_region')}",
            data.get("camera_id"),
            data.get("violation_id"),
            data.get("violation_value"),
            data.get('skill_value'),
            data.get('datetime')
        )  

    @classmethod
    def parse_camerus2(cls, data: dict) -> tuple:
        transport:dict = data.get("transport")
        numbers = transport.get("numbers")
        camera:dict = data.get('camera')
        violation: dict = data.get('violation')
        skill: dict = data.get('skill')
        return (
            f"{numbers[0]}{transport.get('chars')}{numbers[1:]}{data.get('region')}",
            camera.get("id"),
            violation.get('id'),
            violation.get('value'),
            skill.get('value'),
            datetime(**data.get('datetime'))
        )
    
    @classmethod
    def parse_camerus3(cls, data: dict) -> tuple:
        camera:dict = data.get('camera')
        violation: dict = data.get('violation')
        return (
            data.get('transport'),
            camera.get("id"),
            violation.get('id'),
            violation.get('value'),
            data.get('skill'),
            datetime.fromtimestamp(float(data.get('datetime')), tz=None)
        )

    @classmethod
    async def parse(cls, model: Type[BaseModel], model_name: str) -> dict:
        values = getattr(cls, f"parse_{model_name}")(model.model_dump())
        keys = (
            "transport",
            "camera_id",
            "violation_id",
            "violation_value",
            'skill_value',
            'case_timestamp'
        )
        return {
            key:value 
            for 
                key, value
            in 
                zip(keys, values)
        }


class SCoordsGPS(BaseModel):
    latitude: Annotated[float, Query(ge= -90, le=90, description="GPS latitude")]
    longitude: Annotated[float, Query(ge= -180, le=180, description="GPS longitude")]

class SCameraRegist(BaseModel):
    GPScoords: Annotated[SCoordsGPS, Query(title="GPS coordinates")]
    CameraType: Annotated[str, Query()]
    description: Annotated[str, Query(max_length=100)]

    @validator("CameraType")
    def check_camera_type(cls, value):
        if value not in (pattern:=DynamicModels.camerus_pattern_list):
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