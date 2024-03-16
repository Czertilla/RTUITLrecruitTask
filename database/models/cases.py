from sqlalchemy import DateTime, ForeignKey
from .base import Base
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column

class CaseORM(Base):
    __tablename__ = "cases"

    transport: Mapped[str]
    owner_id: Mapped[UUID|None] = mapped_column(ForeignKey("carowners.ID"))
    camera_id: Mapped[UUID] = mapped_column(ForeignKey("cameras.ID"))
    violation_id: Mapped[UUID] = mapped_column(ForeignKey("violations.ID"))
    violation_value: Mapped[str] = mapped_column(default='')
    skill_value: Mapped[int]
    datetime: Mapped[DateTime]

