from repositories.cameras import CameraRepo
from repositories.cases import CaseRepo
from repositories.files import FileRepo
from repositories.votes import VoteRepo
from units_of_work._unit_of_work import UnitOfWork


class CaseUOW(UnitOfWork):
    async def __aenter__(self):
        rtrn = await super().__aenter__()
        self.cameras = CameraRepo(self.session)
        self.cases = CaseRepo(self.session)
        self.files = FileRepo(self.session)
        self.votes = VoteRepo(self.session)
        return rtrn
