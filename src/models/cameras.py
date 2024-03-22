from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..database.engine.base import Base

class CameraOrm(Base):
    __tablename__ = "cameras"

    latitude: Mapped[float]
    longitude: Mapped[float]
    description: Mapped[str] = mapped_column(default="")
    cam_type: Mapped[str] = mapped_column(ForeignKey("dependencies.id", ondelete="RESTRICT"))
