from typing import TYPE_CHECKING
from database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models import cases
from database.models import votes
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

if TYPE_CHECKING:
    from .cases import CaseORM
    from .votes import VoteORM

class UserORM(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(unique=True)
    role: Mapped[str] = mapped_column(default="unverified")
    wallet: Mapped[float] = mapped_column(default=0.)
    skill: Mapped[int] = mapped_column(default=1)

    cases: Mapped[list["CaseORM"]] = relationship(
        secondary="votes",
        back_populates="users",
        viewonly=True
    )
    case_associations: Mapped[list["VoteORM"]] = relationship(
        back_populates="user_table"
    )
