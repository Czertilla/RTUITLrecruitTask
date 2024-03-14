from pydantic import BaseModel, ValidationError, validator
from typing import Annotated
from fastapi import Depends, Query
from .dynamic import DynamicModels

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
    # photo: UploadFilee
    metadata: bytes
