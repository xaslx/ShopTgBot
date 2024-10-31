from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @abstractmethod
    async def add(self, **kwargs):
        pass

    @abstractmethod
    async def delete(self, **kwargs):
        pass

    @abstractmethod
    async def find_one_or_none(self, **kwargs):
        pass

    @abstractmethod
    async def find_all(self, **kwargs):
        pass