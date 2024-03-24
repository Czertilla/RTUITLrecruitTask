from units_of_work.unit_of_work import UnitOfWork
from utils.absract.unit_of_work import ABCUnitOfWork


class BaseService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow: UnitOfWork = uow