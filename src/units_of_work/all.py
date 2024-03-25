from repositories.camerus import CamerusRepo
from repositories.cameras import CameraRepo
from repositories.carowners import CarOwnerRepo
from repositories.cases import CaseRepo
from repositories.export import ExportRepo
from repositories.files import FileRepo
from repositories.users import UserRepo
from repositories.violations import ViolationRepo
from units_of_work._unit_of_work import UnitOfWork

class AllUOW(UnitOfWork):
    async def __aenter__(self):
        rtrn = await super().__aenter__()
        self.cameras = CameraRepo(self.session)
        self.camerus = CamerusRepo(self.session)
        self.cases = CaseRepo(self.session)
        self.car_owners = CarOwnerRepo(self.session)
        self.export = ExportRepo(self.session)
        self.files = FileRepo(self.session)
        self.users = UserRepo(self.session)
        self.violations = ViolationRepo(self.session)
        return rtrn
