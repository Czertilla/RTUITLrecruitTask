from database import new_session
from utils.absract.unit_of_work import ABCUnitOfWork


class UnitOfWork(ABCUnitOfWork):
    def __init__(self):
        self.new_session = new_session


    async def __aenter__(self):
        self.session = self.new_session()



    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()


    async def commit(self):
        await self.session.commit()


    async def rollback(self):
        await self.session.rollback()
