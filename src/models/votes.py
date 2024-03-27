from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import UUID, Column, ForeignKey, UniqueConstraint, Table
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import func

if TYPE_CHECKING:
    from .users import UserORM
    from .cases import CaseORM

# VoteORM = Table(
#     "votes",
#     Base.metadata,
#     Column("id", UUID, primary_key=True),
#     Column("case_id", ForeignKey("cases.id"), nullable=False),
#     Column("user_id", ForeignKey("user.id"), nullable=False),
    
#     UniqueConstraint("case_id", "user_id", name="idx_case_user_constraint")
# )
class VoteORM(Base):
    __tablename__ = "votes"
    __table_args__ = (
        UniqueConstraint(
            "case_id",
            "user_id",
            name="idx_case_user_constraint",
        ),
    )
    
    case_id: Mapped[UUID] = mapped_column(ForeignKey("cases.id"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    justify: Mapped[bool] = mapped_column(nullable=True, default=None)
    timestamp: Mapped[datetime] = mapped_column(default=func.now())
    
    case_model: Mapped["CaseORM"] = relationship(back_populates="votes_list")

    user_model: Mapped["UserORM"] = relationship(back_populates="votes_list")

