from repositories.camerus import CamerusRepo
from units_of_work.unit_of_work import UnitOfWork

class CamerusUOW(UnitOfWork):
    async def __aenter__(self):
        rtrn = await super().__aenter__()
        self.camerus = CamerusRepo(self.session)
        return rtrn