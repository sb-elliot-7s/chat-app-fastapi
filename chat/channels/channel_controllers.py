from fastapi import APIRouter, Depends
from .channel_presenter import ChannelPresenter
from .channel_schemas import CreateChannelSchema, UpdateChannelSchema
from .channel_deps import response_data, get_customer, get_repository_service

channel_controllers = APIRouter(prefix='/channels', tags=['channels'])


@channel_controllers.post(**response_data.get('subscribe'))
async def subscribe(
        channel_slug: str, repository=Depends(get_repository_service),
        customer=Depends(get_customer)
):
    return await ChannelPresenter(**repository) \
        .subscribe(channel_slug=channel_slug, customer_id=customer.id)


@channel_controllers.delete(**response_data.get('unsubscribe'))
async def unsubscribe(
        channel_id: int, customer=Depends(get_customer),
        repository=Depends(get_repository_service),
):
    return await ChannelPresenter(**repository) \
        .unsubscribe(channel_id=channel_id, customer_id=customer.id)


@channel_controllers.get(**response_data.get('channels'))
async def get_channels(
        customer=Depends(get_customer),
        repository=Depends(get_repository_service),
        limit: int | None = 20, offset: int | None = 0
):
    return await ChannelPresenter(**repository) \
        .get_channels(customer_id=customer.id, limit=limit, offset=offset)


@channel_controllers.post(**response_data.get('create_channels'))
async def create_channel(
        channel_data: CreateChannelSchema,
        customer=Depends(get_customer),
        repository=Depends(get_repository_service),
):
    return await ChannelPresenter(**repository) \
        .create_channel(customer_id=customer.id, channel_data=channel_data)


@channel_controllers.delete(**response_data.get('delete_channels'))
async def delete_channel(
        channel_slug: str, customer=Depends(get_customer),
        repository=Depends(get_repository_service),
):
    return await ChannelPresenter(**repository) \
        .delete_channel(customer_id=customer.id, channel_slug=channel_slug)


@channel_controllers.patch(**response_data.get('update_channel'))
async def update_channel(
        updated_data: UpdateChannelSchema,
        channel_slug: str, customer=Depends(get_customer),
        repository=Depends(get_repository_service),
):
    return await ChannelPresenter(**repository) \
        .update_channel(updated_data=updated_data, channel_slug=channel_slug,
                        customer_id=customer.id)


@channel_controllers.get(**response_data.get('channel'))
async def get_channel(
        channel_slug: str, repository=Depends(get_repository_service),
):
    return await ChannelPresenter(**repository) \
        .get_channel(channel_slug=channel_slug)
