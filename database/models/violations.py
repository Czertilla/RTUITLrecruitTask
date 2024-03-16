from sqlalchemy import UniqueConstraint
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column

class ViolationORM(Base):
    __tablename__ = "violations"

    violation_type: Mapped[str] = mapped_column(unique=True)
    fine: Mapped[float]

    
    __table_args__ = (UniqueConstraint("ID", 'violation_type', name='export_constraint'),)