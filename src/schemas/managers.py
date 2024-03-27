from typing import Annotated
from uuid import UUID
from pydantic import BaseModel, Field

class SImportExelRespose(BaseModel):
    added: int
    updated: list[str]
    invalid: list[str]

class SVerifyResponse(BaseModel):
    status: Annotated[str, Field(default="verified")]
