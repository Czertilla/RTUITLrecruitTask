from typing import Any
from uuid import uuid4, UUID
from sqlalchemy.types import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    ID: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    type_annotation_map = {
        dict[str, Any]: JSON
    }