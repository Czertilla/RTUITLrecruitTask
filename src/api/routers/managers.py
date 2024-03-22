from typing import TYPE_CHECKING, Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from logging import getLogger

from pydantic import Field
from database.repositories.export import ExportRepo
from database.repositories.users import UserRepo
from schemas.auth import UserRead
from schemas.managers import SImportExelRespose, SVerifyResponse
from utils.importer import import_excel
from app.auth.core import get_user_manager
from app.auth.auth import fastapi_users

from models.users import UserORM

logger = getLogger(__name__)

manager = fastapi_users.current_user(superuser=True)
managers = APIRouter(prefix="/managers", tags=["managers"])
usermanager = get_user_manager()

export_repo_dep = {repo.orm.__tablename__: repo for repo in ExportRepo.__subclasses__()}
export_tables_pattern = '|'.join(export_repo_dep.keys())

@managers.post("/import/{table}/upload-file")
async def import_from_xlsx(
    table: Annotated[str, Field(pattern=export_tables_pattern)],
    file: UploadFile,
    current_user: UserORM = Depends(manager)
) -> SImportExelRespose:
    repository = export_repo_dep.get(table)
    data = import_excel(await file.read())
    success = (await repository.export(data))
    return success

@managers.post("/verify")
async def verify_user(id: UUID, current_user: UserORM = Depends(manager)) -> SVerifyResponse:
    user = await UserRepo.verify(id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return {
        "status": "OK"
    }
    