from typing import TYPE_CHECKING
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import cases
from models import votes
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
6
if TYPE_CHECKING:
    from .cases import CaseORM
    from .votes import VoteORM

class UserORM(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(unique=True)
    role: Mapped[str] = mapped_column(default="unverified")
    wallet: Mapped[float] = mapped_column(default=0.)
    skill: Mapped[int] = mapped_column(default=1)

    cases_list: Mapped[list["CaseORM"]] = relationship(
        secondary="votes",
        back_populates="users_list",
        viewonly=True
    )
    votes_list: Mapped[list["VoteORM"]] = relationship(
        back_populates="user_model"
    )
