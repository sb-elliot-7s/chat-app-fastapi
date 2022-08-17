from abc import ABC, abstractmethod


class CustomerRepositoriesInterface(ABC):

    @abstractmethod
    async def save_user(self, username: str, password: str): pass

    @abstractmethod
    async def receive_customer_by_username(self, username: str): pass
