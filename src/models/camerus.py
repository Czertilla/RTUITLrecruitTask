from uuid import uuid4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from ..database.engine.base import Base
from typing import Any

class DependenciesOrm(Base):
    __tablename__ = "dependencies"

    key: Mapped[str]
    value_type: Mapped[str]
    enclosure: Mapped[UUID|None] = mapped_column(ForeignKey("dependencies.id"))
    destination: Mapped[str|None]
    field_attrs: Mapped[dict[str, Any]] = mapped_column(default={})

