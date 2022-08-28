import uuid
from dataclasses import dataclass

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert

from image_service.interfaces.image_service_interface import ImageServiceInterface
from ..auth.models import Customers, CustomerImage
from .schemas import UpdateCustomerSchema

from .interfaces.profile_repositories_interface import ProfileRepositoriesInterface
from .exceptions import ProfileExceptions
import aiohttp
from settings import get_settings


@dataclass
class ProfileRepositories(ProfileRepositoriesInterface):
    session: AsyncSession

    async def update_profile_image(
            self, images: list[UploadFile] | None,
            customer_id: int,
            file_service: ImageServiceInterface
    ):
        if images:
            for image in images:
                filename = f'{uuid.uuid4()}.{image.filename}'
                await file_service.write_image(file=image, filename=filename)
                stmt = insert(CustomerImage) \
                    .values(photo=filename, customer_id=customer_id)
                await self.session.execute(statement=stmt)
                await self.session.commit()

    async def delete_image(
            self, image_name: str, customer_id: int,
            image_service: ImageServiceInterface
    ):
        await image_service.delete_image(filename=image_name)
        stmt = delete(CustomerImage) \
            .where(CustomerImage.photo == image_name,
                   CustomerImage.customer_id == customer_id)
        await self.session.execute(statement=stmt)
        await self.session.commit()

    async def get_customer(self, customer_id: int):
        stmt = select(Customers).where(Customers.id == customer_id)
        result = await self.session.execute(statement=stmt)
        return result.scalars().first()

    async def __check_username_exists(self, username: str | None = None):
        if username:
            username_stmt = select(Customers.id) \
                .where(Customers.username == username)
            check_customer = await self.session.execute(statement=username_stmt)
            if check_customer.first():
                raise ProfileExceptions().username_exists

    @staticmethod
    async def __create_new_token(username: str):
        async with aiohttp.ClientSession() as session:
            options = {
                'url': get_settings().base_url + '/auth/receive_token/',
                'json': {'username': username}
            }
            async with session.post(**options) as response:
                if response.status == 201:
                    return await response.json()

    async def update_customer(self, customer_id: int, data: UpdateCustomerSchema):
        await self.__check_username_exists(username=data.username)
        upd_stmt = update(Customers) \
            .where(Customers.id == customer_id) \
            .values(**data.dict(exclude_none=True)) \
            .returning(Customers)
        _ = await self.session.execute(statement=upd_stmt)
        await self.session.commit()
        if data.username:
            customer = await self.get_customer(customer_id=customer_id)
            return await self.__create_new_token(username=customer.username)
        return {'detail': f'User {customer_id} updated'}

    async def delete_customer(self, customer_id: int):
        stmt = delete(Customers).where(Customers.id == customer_id)
        _ = await self.session.execute(statement=stmt)
        await self.session.commit()
