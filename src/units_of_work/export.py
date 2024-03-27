from repositories.export import ExportRepo
from units_of_work._unit_of_work import UnitOfWork

class ExportUOW(UnitOfWork):
    async def __aenter__(self):
        rtrn = await super().__aenter__()
        self.export_repo_dep = {repo.model.__tablename__: repo for repo in ExportRepo.__subclasses__()}
        self.export = ExportRepo(self.session)
        for name, repo in self.export_repo_dep.items():
            setattr(self, name, repo(self.session))
        return rtrn