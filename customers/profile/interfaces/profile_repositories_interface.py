from abc import ABC, abstractmethod

from fastapi import UploadFile

from image_service.interfaces.image_service_interface import ImageServiceInterface
from ..schemas import UpdateCustomerSchema


class ProfileRepositoriesInterface(ABC):

    @abstractmethod
    async def get_customer(self, customer_id: int): pass

    @abstractmethod
    async def update_customer(self, customer_id: int, data: UpdateCustomerSchema):
        pass

    @abstractmethod
    async def delete_customer(self, customer_id: int): pass

    @abstractmethod
    async def update_profile_image(
            self, images: list[UploadFile] | None,
            customer_id: int, file_service: ImageServiceInterface
    ):
        pass

    @abstractmethod
    async def delete_image(
            self, image_name: str, customer_id: int,
            image_service: ImageServiceInterface
    ):
        pass
