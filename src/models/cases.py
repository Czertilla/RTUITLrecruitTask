from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, func
from database import Base
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

if TYPE_CHECKING:
    from .users import UserORM
    from .votes import VoteORM

class CaseStatus:
    INITIATED = "initiated"
    EXTENDET = "extendet"
    JUSTIFIED = "justified"
    CONVICTED = "convicted"

class CaseORM(Base):
    __tablename__ = "cases"

    transport: Mapped[str]
    photo_id: Mapped[UUID|None] = mapped_column(ForeignKey("files.id"), default=None)
    owner_id: Mapped[UUID|None] = mapped_column(ForeignKey("car_owners.id"))
    camera_id: Mapped[UUID] = mapped_column(ForeignKey("cameras.id"))
    violation_id: Mapped[UUID] = mapped_column(ForeignKey("violations.id"))
    violation_value: Mapped[str] = mapped_column(default='')
    skill_value: Mapped[int]
    case_timestamp: Mapped[datetime]
    status: Mapped[str] = mapped_column(default=CaseStatus.INITIATED)
    status_timestamp: Mapped[datetime] = mapped_column(default=func.now())

    users_list: Mapped[list["UserORM"]] = relationship(
        secondary="votes", 
        back_populates="cases_list",
        viewonly=True
    )

    votes_list: Mapped[list["VoteORM"]] = relationship(
        back_populates="case_model"
    )

