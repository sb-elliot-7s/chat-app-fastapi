from fastapi import status, Depends
from permissions import CustomerPermission
from customers.auth.token_service import TokenService
from .schemas import ChannelSchema
from database import get_db_session
from .repositories import ChannelRepositories


async def get_customer(
        customer=Depends(CustomerPermission(token_service=TokenService())
                         .get_current_user)
):
    yield customer


async def get_repository_service(session=Depends(get_db_session)):
    yield {
        'repository': ChannelRepositories(session=session)
    }


response_data = {
    'subscribe': {
        'path': '/subscribe/{channel_slug}',
        'status_code': status.HTTP_201_CREATED
    },
    'unsubscribe': {
        'path': '/unsubscribe/{channel_slug}',
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
    'check-user': {
        'path': '/check-user/{customer_id}',
        'status_code': status.HTTP_200_OK,
    }
}
