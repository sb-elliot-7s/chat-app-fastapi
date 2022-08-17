from .interfaces.repositories_interface import CustomerRepositoriesInterface
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from .models import Customers


@dataclass
class CustomerRepositories(CustomerRepositoriesInterface):
    session: AsyncSession

    async def save_user(self, username: str, password: str):
        stmt = insert(Customers).values(username=username, password=password)
        _ = await self.session.execute(statement=stmt)
        await self.session.commit()

    async def receive_customer_by_username(self, username: str):
        stmt = select(Customers).where(Customers.username == username)
        result = await self.session.execute(statement=stmt)
        return result.scalars().first()
