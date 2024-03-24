from utils.abstract_repo import AbstractRepository

class BaseService:
    def __init__(self, repository: AbstractRepository) -> None:
        self.repository: AbstractRepository = repository()
