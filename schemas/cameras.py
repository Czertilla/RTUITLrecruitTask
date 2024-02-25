from pydantic import BaseModel
from typing import Annotated
from fastapi import Query
from uuid import UUID
from datetime import datetime

class BaseCamerus(BaseModel):
    ...

class camerus1(BaseCamerus):
    transport_chars: Annotated[str, Query(pattern="[A-Z]{3}")]
    transport_numbers: Annotated[str, Query(pattern="[0-9]{3}")]
    transport_region: Annotated[str, Query(pattern="[0-9]{2}")]
    camera_id: UUID
    violation_id: UUID
    violation_value: Annotated[str, Query(description="circumstances of the violation")]
    skill_value: Annotated[int, Query(ge=1, le=100)]
    datetime: Annotated[datetime, Query()]

class SCoordsGPS (BaseModel):
    latitude: Annotated[float, Query(ge= -90, le=90, description="GPS latitude")]
    longitude: Annotated[float, Query(ge= -180, le=180, description="GPS longitude")]

class SCameraRegist (BaseModel):
    GPScoords: Annotated[SCoordsGPS, Query(title="GPS coordinates")]
    CameraType: Annotated[str, Query(pattern='|'.join([cls.__name__ for cls in BaseCamerus.__subclasses__()]))]
