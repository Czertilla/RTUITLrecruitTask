
from datetime import datetime
from typing import Annotated
from fastapi import Query
from pydantic import BaseModel, Field


class SCaseGet(BaseModel):
    transport: Annotated[str, Field(pattern="[0-9][A-Z]{3}[0-9]{4}")]
    violation_type: str
    violation_value: Annotated[str, Field(max_length=100)]
    case_timestamp: datetime
    
    class Config:
        from_atributes = True

class SGetCaseResponse(BaseModel):
    photo: bytes
    metadata: SCaseGet

    class Config:
        from_atributes = True

class SVoteRequest(BaseModel):
    vote: Annotated[str, Query(pattern=f"justify|convinct")]

class SVoteResponce(BaseModel):
    status: str = 'OK'
