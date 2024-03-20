from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from database.models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import func

if TYPE_CHECKING:
    from .users import UserORM
    from .cases import CaseORM

class VoteORM(Base):
    __tablename__ = "votes"

    
    case_id: Mapped[UUID] = mapped_column(ForeignKey("cases.id"), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)
    justify: Mapped[bool] = mapped_column(nullable=True, default=False)
    timestamp: Mapped[datetime] = mapped_column(default=func.now())

    user_table: Mapped["UserORM"] = relationship(back_populates="case_associations")

    case_table: Mapped["CaseORM"] = relationship(back_populates="user_associations")
