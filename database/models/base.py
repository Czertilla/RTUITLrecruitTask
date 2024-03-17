from typing import Any
from uuid import uuid4, UUID
from sqlalchemy.types import JSON, DateTime
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, column_property
from sqlalchemy.ext.declarative import declared_attr

class IdMinxin:
    @declared_attr
    def ID(cls) -> Mapped[UUID]:
        return mapped_column(primary_key=True, default=uuid4)

class Base(DeclarativeBase, IdMinxin):
    __abstract__ = True
    
    type_annotation_map = {
        dict[str, Any]: JSON,
        datetime: DateTime(timezone=True)
    }
