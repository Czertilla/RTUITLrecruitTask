from uuid import UUID

from sqlalchemy import select
from models.files import FileORM
from database import new_session
from models.files import FileORM


class FileRepo():
    ...