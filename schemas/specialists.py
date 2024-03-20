from typing import Annotated
from fastapi import Query, UploadFile
from pydantic import BaseModel
from database.models.cases import CaseStatus
from schemas.cameras import SCaseInsert

class SGetCaseResponce(BaseModel):
    photo: bytes
    metadata: SCaseInsert
    ...

class SVoteRequest(BaseModel):
    vote: Annotated[str, Query(pattern=f"justify|convinct")]

class SVoteResponce(BaseModel):
    status: str = 'OK'