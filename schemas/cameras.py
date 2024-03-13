from pydantic import BaseModel
from typing import Annotated
from fastapi import Depends, Query, UploadFile
from .dynamic import DynamicModels

class SCoordsGPS(BaseModel):
    latitude: Annotated[float, Query(ge= -90, le=90, description="GPS latitude")]
    longitude: Annotated[float, Query(ge= -180, le=180, description="GPS longitude")]

print("schemas")
class SCameraRegist(BaseModel):
    GPScoords: Annotated[SCoordsGPS, Query(title="GPS coordinates")]
    CameraType: Annotated[str, Depends(DynamicModels.get_pattern)]
    description: Annotated[str, Query(max_length=100)]

class SCameraCase (BaseModel):
    # photo: UploadFile
    metadata: bytes
