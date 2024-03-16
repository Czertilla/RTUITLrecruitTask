from typing import Annotated
from fastapi import APIRouter, UploadFile
from logging import getLogger

from pydantic import Field
from database.repositories.export import ExportRepo
from schemas.managers import SImportExelRespose
from utils.importer import import_excel

logger = getLogger(__name__)

managers = APIRouter(prefix="/managers")

export_repo_dep = {repo.orm.__tablename__: repo for repo in ExportRepo.__subclasses__()}
export_tables_pattern = '|'.join(export_repo_dep.keys())

@managers.post("/import/{table}/upload-file")
async def import_from_xlsx(
    table: Annotated[str, Field(pattern=export_tables_pattern)],
    file: UploadFile
) -> SImportExelRespose:
    repository = export_repo_dep.get(table)
    data = import_excel(await file.read())
    success = (await repository.export(data))
    return success
