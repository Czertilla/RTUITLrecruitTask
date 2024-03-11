from pydantic import BaseModel
from typing import Annotated
from fastapi import Query, UploadFile
from uuid import UUID
from datetime import datetime

class BaseCamerus(BaseModel):
    ...

class SCoordsGPS(BaseModel):
    latitude: Annotated[float, Query(ge= -90, le=90, description="GPS latitude")]
    longitude: Annotated[float, Query(ge= -180, le=180, description="GPS longitude")]

class SCameraRegist(BaseModel):
    GPScoords: Annotated[SCoordsGPS, Query(title="GPS coordinates")]
    CameraType: Annotated[str, Query(pattern='|'.join([cls.__name__ for cls in BaseCamerus.__subclasses__()]))]
    description: Annotated[str, Query(max_length=100)]

class SCameraCase (BaseModel):
    # photo: UploadFile
    metadata: dict

