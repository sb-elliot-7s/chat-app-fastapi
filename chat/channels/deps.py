from fastapi import status, Depends
from permissions import CustomerPermission
from customers.auth.token_service import TokenService
from .schemas import ChannelSchema, CreateChannelSchema, UpdateChannelSchema
from .repositories import ChannelRepositories

from .presenter import ChannelPresenter
from database import get_db_session


async def get_customer(
        customer=Depends(CustomerPermission(token_service=TokenService())
                         .get_current_user)
):
    yield customer


# async def get_repository_service(session=Depends(get_db_session)):
#     yield {
#         'repository': ChannelRepositories(session=session)
#     }


async def get_presenter(session=Depends(get_db_session)):
    presenter = ChannelPresenter(
        repository=ChannelRepositories(session=session))
    yield presenter


async def get_channel_customer(channel_id: int, customer_id: int) -> dict:
    return {'channel_id': channel_id, 'customer_id': customer_id}


async def get_limit_offset_user(user_id: int, limit: int, offset: int) -> dict:
    return {'customer_id': user_id, 'limit': limit, 'offset': offset}


async def get_slug_customer(channel_slug: str, customer_id: int) -> dict:
    return {'channel_slug': channel_slug, 'customer_id': customer_id}


async def get_updated_data_slug_customer(updated_data: UpdateChannelSchema,
                                         channel_slug: str,
                                         customer_id: int) -> dict:
    return {
        'updated_data': updated_data,
        'channel_slug': channel_slug,
        'customer_id': customer_id
    }


async def get_create_data_customer(customer_id: int,
                                   channel_data: CreateChannelSchema) -> dict:
    return {'customer_id': customer_id, 'channel_data': channel_data}


response_data = {
    'subscribe': {
        'path': '/subscribe/{channel_slug}',
        'status_code': status.HTTP_201_CREATED
    },
    'unsubscribe': {
        'path': '/unsubscribe/{channel_id}',
        'status_code': status.HTTP_204_NO_CONTENT
    },
    'channels': {
        'path': '/',
        'status_code': status.HTTP_200_OK,
        # 'response_model': list[ChannelSchema]
    },
    'create_channels': {
        'path': '/',
        'status_code': status.HTTP_201_CREATED,
    },
    'delete_channels': {
        'path': '/{channel_slug}',
        'status_code': status.HTTP_204_NO_CONTENT,
    },
    'update_channel': {
        'path': '/{channel_slug}',
        'status_code': status.HTTP_200_OK,
    },
    'channel': {
        'path': '/{channel_slug}',
        'status_code': status.HTTP_200_OK,
        'response_model': ChannelSchema
    },
    'check_user': {
        'path': '/check-user/{customer_id}/channel/{channel_id}',
        'status_code': status.HTTP_200_OK,
    }
}
