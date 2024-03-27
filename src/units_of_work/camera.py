from repositories.cameras import CameraRepo
from repositories.camerus import CamerusRepo
from units_of_work._unit_of_work import UnitOfWork

class CameraUOW(UnitOfWork):
    async def __aenter__(self):
        rtrn = await super().__aenter__()
        self.cameras = CameraRepo(self.session)
        self.camerus = CamerusRepo(self.session)
        return rtrn
