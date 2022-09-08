from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from permissions import CustomerPermission
from customers.auth.token_service import TokenService
from .states import StateHandler
from .utils import last_messages, get_channel
from .deps import response_data, get_presenter, get_message_search_presenter, \
    get_message_elastic_service
from .schemas import SearchMessageSchema
from .presenter import MessageSearchPresenter, MessagePresenter

message_controllers = APIRouter(prefix='/messages', tags=['messages'])


@message_controllers.post(**response_data.get('search'))
def search_messages(
        options: SearchMessageSchema,
        elastic_receiver=Depends(get_message_elastic_service),
        search_presenter: MessageSearchPresenter = Depends(
            get_message_search_presenter)
):
    return search_presenter \
        .search_messages(options=options, receiver=elastic_receiver)


@message_controllers.get(**response_data.get('my_messages_from_channels'))
async def my_messages_from_channel(
        channel_id: int,
        presenter: MessagePresenter = Depends(get_presenter),
        limit: int = 20, offset: int = 0,
        customer=Depends(
            CustomerPermission(token_service=TokenService()).get_current_user)
):
    return await presenter.get_messages(
        channel_id=channel_id,
        customer_id=customer.id,
        limit=limit,
        offset=offset,
        is_chat=False
    )


@message_controllers.delete(**response_data.get('delete_message'))
async def delete_message(
        message_id: int,
        presenter=Depends(get_presenter),
        customer=Depends(
            CustomerPermission(token_service=TokenService()).get_current_user)
):
    await presenter \
        .delete_message(message_id=message_id, customer_id=customer.id)


@message_controllers.get(**response_data.get('get_message'))
async def get_message(
        message_id: int,
        presenter=Depends(get_presenter),
        customer=Depends(
            CustomerPermission(token_service=TokenService()).get_current_user)
):
    return await presenter \
        .get_message(message_id=message_id, customer_id=customer.id)


@message_controllers.websocket(**response_data.get('ws_chat'))
async def chat(
        channel_slug: str,
        websocket: WebSocket,
        limit: int = 20,
        offset: int = 0,
        presenter=Depends(get_presenter),
        customer=Depends(
            CustomerPermission(token_service=TokenService())
            .jwt_websocket_current_user)
):
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
