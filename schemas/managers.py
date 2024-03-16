from pydantic import BaseModel

class SImportExelRespose(BaseModel):
    added: int
    updated: list[str]
    invalid: list[str]