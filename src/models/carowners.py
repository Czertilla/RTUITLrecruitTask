from sqlalchemy import UniqueConstraint
from ..database.engine.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class CarOwnerORM(Base):
    __tablename__ = "car_owners"

    car_number: Mapped[str] = mapped_column(unique=True)
    phone_number: Mapped[str|None]
    email: Mapped[str|None]
    tg: Mapped[str|None]
    vk: Mapped[str|None]
