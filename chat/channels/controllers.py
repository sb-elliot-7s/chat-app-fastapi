from fastapi import APIRouter, Depends
from .presenter import ChannelPresenter
from .schemas import CreateChannelSchema, UpdateChannelSchema
from .deps import response_data, get_customer, get_presenter, \
    get_slug_customer, get_channel_customer, get_limit_offset_user, \
    get_create_data_customer, get_updated_data_slug_customer

channel_controllers = APIRouter(prefix='/channels', tags=['channels'])


@channel_controllers.post(**response_data.get('subscribe'))
async def subscribe(
        channel_slug: str,
        customer=Depends(get_customer),
        presenter: ChannelPresenter = Depends(get_presenter)
):
    data: dict = await get_slug_customer(channel_slug, customer.id)
    return await presenter.subscribe(**data)


@channel_controllers.delete(**response_data.get('unsubscribe'))
async def unsubscribe(
        channel_id: int, customer=Depends(get_customer),
        presenter: ChannelPresenter = Depends(get_presenter)
):
    data: dict = await get_channel_customer(channel_id, customer.id)
    return await presenter.unsubscribe(**data)


@channel_controllers.get(**response_data.get('check_user'))
async def check_user(
        customer_id: int,
        channel_id: int,
        presenter: ChannelPresenter = Depends(get_presenter)
):
    data: dict = await get_channel_customer(channel_id, customer_id)
    return await presenter.check_if_user_in_subscribed(**data)


@channel_controllers.get(**response_data.get('channels'))
async def get_channels(
        customer=Depends(get_customer),
        presenter: ChannelPresenter = Depends(get_presenter),
        limit: int | None = 20, offset: int | None = 0
):
    data: dict = await get_limit_offset_user(customer.id, limit, offset)
    return await presenter.get_channels(**data)


@channel_controllers.post(**response_data.get('create_channels'))
async def create_channel(
        channel_data: CreateChannelSchema,
        customer=Depends(get_customer),
        presenter: ChannelPresenter = Depends(get_presenter),
):
    data: dict = await get_create_data_customer(customer.id, channel_data)
    return await presenter.create_channel(**data)


@channel_controllers.delete(**response_data.get('delete_channels'))
async def delete_channel(
        channel_slug: str, customer=Depends(get_customer),
        presenter: ChannelPresenter = Depends(get_presenter),
):
    data: dict = await get_slug_customer(channel_slug, customer.id)
    return await presenter.delete_channel(**data)


@channel_controllers.patch(**response_data.get('update_channel'))
async def update_channel(
        updated_data: UpdateChannelSchema,
        channel_slug: str, customer=Depends(get_customer),
        presenter: ChannelPresenter = Depends(get_presenter),
):
    data: dict = await get_updated_data_slug_customer(
        updated_data, channel_slug, customer.id)
    return await presenter.update_channel(**data)


@channel_controllers.get(**response_data.get('channel'))
async def get_channel(
        channel_slug: str,
        presenter: ChannelPresenter = Depends(get_presenter),
):
    return await presenter.get_channel(channel_slug=channel_slug)
