from fastapi import APIRouter, Depends, File, UploadFile
from .schemas import UpdateCustomerSchema
from .presenter import ProfilePresenter
from image_service.image_service import ImageService
from .deps import get_customer_data, get_presenter
from .deps import response_data
from settings import get_settings

profile_controllers = APIRouter(prefix='/profile', tags=['profile'])


@profile_controllers.post(**response_data.get('add_image'))
async def add_images(
        images: list[UploadFile] | None = File(None),
        presenter_data=Depends(get_presenter),
        customer=Depends(get_customer_data)
):
    return await ProfilePresenter(**presenter_data).add_images(
        images=images, customer_id=customer.id,
        file_service=ImageService(path=get_settings().profile_image_folder)
    )


@profile_controllers.delete(**response_data.get('delete_image'))
async def delete_image(
        image_name: str, presenter_data=Depends(get_presenter),
        customer=Depends(get_customer_data)
):
    return await ProfilePresenter(**presenter_data).delete_image(
        image_name=image_name, customer_id=customer.id,
        image_service=ImageService(path=get_settings().profile_image_folder)
    )


@profile_controllers.get(**response_data.get('get_customer'))
async def get_customer(customer=Depends(get_customer_data)):
    return customer


@profile_controllers.patch(**response_data.get('update_customer'))
async def update_customer(
        updated_data: UpdateCustomerSchema,
        presenter_data=Depends(get_presenter),
        customer=Depends(get_customer_data)
):
    return await ProfilePresenter(**presenter_data) \
        .update_customer(customer_id=customer.id, data=updated_data)


@profile_controllers.delete(**response_data.get('delete_customer'))
async def delete_customer(
        presenter_data=Depends(get_presenter),
        customer=Depends(get_customer_data)
):
    return await ProfilePresenter(**presenter_data) \
        .delete_customer(customer_id=customer.id)
