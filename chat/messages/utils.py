import aiohttp
from enum import Enum
from .presenter import MessagePresenter
from settings import get_settings
from .schemas import MessageSchema


class METHOD(Enum):
    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    PUT = 'PUT'


async def handler(
        url: str, method: str, json_data: dict | None = None,
        status_code: int = 200, headers: dict | None = None,
):
    base_url: str = get_settings().base_url
    async with aiohttp.ClientSession(base_url=base_url) as session:
        async with session.request(
                url=url, method=method, json=json_data, headers=headers
        ) as response:
            if response.status == status_code:
                return await response.json()


async def get_channel(channel_slug: str):
    data = {
        'url': f'/channels/{channel_slug}',
        'method': METHOD.GET.value,
        'status_code': 200
    }
    return await handler(**data)


async def create_channel(
        channel_name: str, describe_info: str | None, token: str):
    data = {
        'url': '/channels/',
        'method': METHOD.POST.value,
        'status_code': 201,
        'json_data': {
            'channel_name': channel_name,
            'describe_info': describe_info
        },
        'headers': {'AUTHORIZATION': f'bearer {token}'}
    }
    return await handler(**data)


async def check_user_in_subscribes(customer_id: int, channel_id: int):
    data = {
        'url': f'/channels/check-user/{customer_id}/channel/{channel_id}',
        'method': METHOD.GET.value,
        'status_code': 200,
    }
    return await handler(**data)


async def last_messages(
        presenter: MessagePresenter,
        limit: int,
        offset: int,
        channel_id: int,
        sender_id: int | None = None
):
    return [
        MessageSchema.from_orm_to_json(x)
        for x in await presenter.get_messages(
            limit=limit,
            offset=offset,
            customer_id=sender_id,
            channel_id=channel_id
        )
    ]
