from repositories.cameras import CameraRepo
from repositories.cases import CaseRepo
from repositories.files import FileRepo
from repositories.users import UserRepo
from repositories.violations import ViolationRepo
from repositories.votes import VoteRepo
from units_of_work._unit_of_work import UnitOfWork

class UserUOW(UnitOfWork):
    async def __aenter__(self):
        rtrn = await super().__aenter__()
        self.files = FileRepo(self.session)
        self.users = UserRepo(self.session)
        return rtrn

class SpecialistUOW(UserUOW):
    async def __aenter__(self):
        rtrn = await super().__aenter__()
        self.cases = CaseRepo(self.session)
        self.files = FileRepo(self.session)
        self.votes = VoteRepo(self.session)
        self.violations = ViolationRepo(self.session)
        self.users = UserRepo(self.session)
        return rtrn
    
class ManagerUOW(UserUOW):
    async def __aenter__(self):
        rtrn = await super().__aenter__()
        self.cameras = CameraRepo(self.session)
        self.cases = CaseRepo(self.session)
        self.files = FileRepo(self.session)
        self.users = UserRepo(self.session)
        return rtrn
