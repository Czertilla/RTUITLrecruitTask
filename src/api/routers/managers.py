from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from logging import getLogger

from pydantic import Field
from api.dependencies import ExportUOWDep, UserUOWDep
from services.export import ExportService
from repositories.users import UserRepo
from schemas.managers import SImportExelRespose, SVerifyResponse
from api.auth.core import get_user_manager
from api.auth.auth import fastapi_users

from models.users import UserORM
from services.users import UserService

logger = getLogger(__name__)

manager = fastapi_users.current_user(superuser=True)
managers = APIRouter(prefix="/managers", tags=["managers"])
usermanager = get_user_manager()

@managers.post("/import/{table}/upload-file")
async def import_from_xlsx(
    table: Annotated[str, Field(pattern=ExportService.export_tables_pattern)],
    file: UploadFile,
    uow: ExportUOWDep,
    current_user: UserORM = Depends(manager),
) -> SImportExelRespose:
    return await ExportService(uow).export(table, file)

@managers.post("/verify")
async def verify_user(
    id: UUID, 
    uow: UserUOWDep,
    current_user: UserORM = Depends(manager)
) -> SVerifyResponse:
    user = await UserService(uow).verify(id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return {
        "status": "OK"
    }
    