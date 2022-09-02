from enum import Enum
from fastapi import WebSocket
from .presenter import MessagePresenter
from .schemas import UpdateMessageSchema, MessageSchema, CreateMessageSchema
from .utils import check_user_in_subscribes
from .exceptions import MessageExceptions


class MessageType(str, Enum):
    CHAT = 'chat'
    READ = 'read'
    UPDATE = 'update'
    USER_TYPING = 'user_typing'


class StateHandler:

    def __init__(self, websocket: WebSocket, presenter: MessagePresenter):
        self.presenter = presenter
        self.websocket = websocket

    async def update_message(
            self, updated_text: str, message_id: int, customer_id: int
    ):
        updated_message: dict = await self.presenter.update_message(
            message_id=message_id,
            customer_id=customer_id,
            updated_data=UpdateMessageSchema(text=updated_text)
        )
        json_updated_message = MessageSchema(**updated_message).json()
        await self.websocket.send_json(data=json_updated_message)

    async def write_message(
            self, text: str, receiver_id: int, sender_id: int, channel_id: int
    ):
        message: dict = await self.presenter.save_message(
            from_customer_id=sender_id,
            message_data=CreateMessageSchema(
                text=text, to_customer_id=receiver_id
            ),
            channel_id=channel_id
        )
        json_message = MessageSchema(**message).json()
        await self.websocket.send_json(data=json_message)

    async def user_typing(self, sender_username: str):
        data = {
            'username': sender_username,
            'message': 'username typing'
        }
        await self.websocket.send_json(data=data)

    async def check_handle(
            self, obj_data: dict, channel: dict, sender_customer
    ):
        message_type: str = obj_data['type']
        match message_type:
            case MessageType.CHAT.value:
                if not await check_user_in_subscribes(
                        customer_id=sender_customer.id,
                        channel_id=channel['id'],
                        token=self.websocket.headers.get('token')):
                    error: dict = MessageExceptions().not_subscribe_error
                    await self.websocket.send_json(data=error)
                else:
                    text = obj_data['text']
                    receiver_id = obj_data['receiver_id']
                    await self.write_message(
                        channel_id=channel['id'],
                        text=text,
                        receiver_id=receiver_id,
                        sender_id=sender_customer.id
                    )
            case MessageType.USER_TYPING.value:
                await self.user_typing(sender_customer.username)
            case MessageType.UPDATE.value:
                updated_text = obj_data['text']
                message_id = obj_data['message_id']
                await self.update_message(
                    updated_text=updated_text,
                    message_id=message_id,
                    customer_id=sender_customer.id
                )
            case MessageType.READ.value:
                ...
