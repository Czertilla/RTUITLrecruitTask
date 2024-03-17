from sqlalchemy import ForeignKey, func
from .base import Base
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class CaseStatus:
    INITIATED = "initiated"
    EXTENDET = "extendet"
    JUSTIFIED = "justified"
    CONVICTED = "convicted"

class CaseORM(Base):
    __tablename__ = "cases"

    transport: Mapped[str]
    photo_id: Mapped[UUID|None] = mapped_column(ForeignKey("files.ID"), default=None)
    owner_id: Mapped[UUID|None] = mapped_column(ForeignKey("car_owners.ID"))
    camera_id: Mapped[UUID] = mapped_column(ForeignKey("cameras.ID"))
    violation_id: Mapped[UUID] = mapped_column(ForeignKey("violations.ID"))
    violation_value: Mapped[str] = mapped_column(default='')
    skill_value: Mapped[int]
    case_timestamp: Mapped[datetime]
    status: Mapped[str] = mapped_column(default=CaseStatus.INITIATED)
    status_timestamp: Mapped[datetime] = mapped_column(default=func.now())
    justify_votes_count: Mapped[int] = mapped_column(default=0)
    convict_votes_count: Mapped[int] = mapped_column(default=0)

