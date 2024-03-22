from sqlalchemy import UniqueConstraint
from ..database.engine.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class ViolationORM(Base):
    __tablename__ = "violations"

    violation_type: Mapped[str] = mapped_column(unique=True)
    fine: Mapped[float]
