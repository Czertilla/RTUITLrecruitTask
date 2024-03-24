from repositories.cases import CaseRepo
from repositories.files import FileRepo
from units_of_work.unit_of_work import UnitOfWork

class CaseUOW(UnitOfWork):
    async def __aenter__(self):
        rtrn = await super().__aenter__()
        self.cases = CaseRepo(self.session)
        self.files = FileRepo(self.session)
        return rtrn