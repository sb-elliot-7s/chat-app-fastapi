from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from permissions import CustomerPermission
from customers.auth.token_service import TokenService
from .states import StateHandler
from .presenter import MessagePresenter
from .repositories import MessageRepositories
from database import get_db_session
from .utils import last_messages, get_channel
from .deps import response_data

message_controllers = APIRouter(prefix='/messages', tags=['messages'])


@message_controllers.get(**response_data.get('my_messages_from_channels'))
async def my_messages_from_channel(
        channel_id: int,
        session=Depends(get_db_session),
        limit: int = 20, offset: int = 0,
        customer=Depends(
            CustomerPermission(token_service=TokenService()).get_current_user)
):
    presenter = MessagePresenter(MessageRepositories(session=session))
    return await presenter.get_messages(
        channel_id=channel_id,
        customer_id=customer.id,
        limit=limit,
        offset=offset
    )


@message_controllers.delete(**response_data.get('delete_message'))
async def delete_message(
        message_id: int, session=Depends(get_db_session),
        customer=Depends(
            CustomerPermission(token_service=TokenService()).get_current_user)
):
    presenter = MessagePresenter(MessageRepositories(session=session))
    await presenter \
        .delete_message(message_id=message_id, customer_id=customer.id)


@message_controllers.get(**response_data.get('get_message'))
async def get_message(
        message_id: int,
        session=Depends(get_db_session),
        customer=Depends(
            CustomerPermission(token_service=TokenService()).get_current_user)
):
    presenter = MessagePresenter(MessageRepositories(session=session))
    return await presenter \
        .get_message(message_id=message_id, customer_id=customer.id)


@message_controllers.websocket(**response_data.get('ws_chat'))
async def chat(
        channel_slug: str,
        websocket: WebSocket,
        limit: int = 20,
        offset: int = 0,
        session=Depends(get_db_session),
        customer=Depends(
            CustomerPermission(token_service=TokenService())
            .jwt_websocket_current_user)
):
    presenter = MessagePresenter(MessageRepositories(session=session))
    sender_customer = customer
    channel = await get_channel(channel_slug=channel_slug)
    if channel is None:
        raise WebSocketDisconnect
    await websocket.accept()
    messages = await last_messages(
        presenter=presenter, limit=limit, offset=offset,
        channel_id=channel['id']
    )
    await websocket.send_json(data=messages)
    try:
        while True:
            obj_data: dict = await websocket.receive_json()
            await StateHandler(websocket=websocket, presenter=presenter) \
                .check_handle(obj_data=obj_data, channel=channel,
                              sender_customer=sender_customer)
    except WebSocketDisconnect:
        ...
