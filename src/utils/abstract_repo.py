from abc import ABC, abstractmethod

class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError
    
    @abstractmethod
    async def find_by_id():
        raise NotImplementedError

    @abstractmethod
    async def find_all():
        raise NotImplementedError

