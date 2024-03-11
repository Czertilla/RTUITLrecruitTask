from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from .base import Base

class CameraOrm(Base):
    __tablename__ = "cameras"

    latitude: Mapped[float]
    longitude: Mapped[float]
    description: Mapped[str] = mapped_column(default="")
    type: Mapped[str] = mapped_column(ForeignKey("dependencies.key", ondelete="RESTRICT"))
