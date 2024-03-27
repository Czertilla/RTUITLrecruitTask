from typing import TYPE_CHECKING
from uuid import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

if TYPE_CHECKING:
    from models import DependenciesOrm

class CameraOrm(Base):
    __tablename__ = "cameras"

    latitude: Mapped[float]
    longitude: Mapped[float]
    description: Mapped[str] = mapped_column(default="")
    cam_type: Mapped[UUID] = mapped_column(ForeignKey("dependencies.id", ondelete="RESTRICT"))
    camerus: Mapped["DependenciesOrm"] = relationship(back_populates="cams_list")