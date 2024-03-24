from models.camerus import DependenciesOrm
from repositories.cameras import CameraRepo
from units_of_work._unit_of_work import UnitOfWork

class CameraUOW(UnitOfWork):
    async def __aenter__(self):
        rtrn = await super().__aenter__()
        self.cameras = CameraRepo(self.session)
        self.camerus = DependenciesOrm(self.session)
        return rtrn
