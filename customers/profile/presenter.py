from dataclasses import dataclass

from fastapi import UploadFile

from image_service.interfaces.image_service_interface import ImageServiceInterface
from .interfaces.profile_repositories_interface import ProfileRepositoriesInterface
from .schemas import UpdateCustomerSchema


@dataclass
class ProfilePresenter:
    repositories: ProfileRepositoriesInterface

    # async def get_customer(self, customer_id: int):
    #     return await self.repositories.get_customer(customer_id=customer_id)

    async def update_customer(self, customer_id: int, data: UpdateCustomerSchema):
        return await self.repositories.update_customer(
            customer_id=customer_id, data=data)

    async def delete_customer(self, customer_id: int):
        return await self.repositories.delete_customer(customer_id=customer_id)

    async def delete_image(
            self, image_name: str, customer_id: int,
            image_service: ImageServiceInterface
    ):
        return await self.repositories.delete_image(
            image_name=image_name, customer_id=customer_id,
            image_service=image_service
        )

    async def add_images(self, images: list[UploadFile] | None, customer_id: int,
                         file_service: ImageServiceInterface):
        await self.repositories \
            .update_profile_image(images=images, customer_id=customer_id,
                                  file_service=file_service)
