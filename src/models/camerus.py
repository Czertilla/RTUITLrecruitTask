from uuid import uuid4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from database import Base
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from models import CameraOrm

class DependenciesOrm(Base):
    __tablename__ = "dependencies"

    key: Mapped[str]
    value_type: Mapped[str]
    enclosure: Mapped[UUID|None] = mapped_column(ForeignKey("dependencies.id"))
    destination: Mapped[str|None]
    field_attrs: Mapped[dict[str, Any]] = mapped_column(default={})
    cams_list: Mapped[list["CameraOrm"]] = relationship(back_populates="camerus")
 