from enum import Enum
from fastapi import WebSocket
from .presenter import MessagePresenter
from .schemas import UpdateMessageSchema, MessageSchema, CreateMessageSchema
from .utils import check_user_in_subscribes
from .exceptions import MessageExceptions
from .utils import last_messages
from settings import get_settings
from .elastic_client import MessageElasticService, ElasticClient


class MessageType(str, Enum):
    CHAT = 'chat'
    READ = 'read'
    UPDATE = 'update'
    USER_TYPING = 'user_typing'


class StateHandler:

    def __init__(self, websocket: WebSocket, presenter: MessagePresenter):
        self.presenter = presenter
        self.websocket = websocket

    async def read_message(
            self, channel_id: int, offset: int = 20, limit: int = 20):
        messages = await last_messages(
            presenter=self.presenter,
            channel_id=channel_id,
            offset=offset,
            limit=limit,
        )
        await self.websocket.send_json(data=messages)

    async def update_message(
            self, updated_text: str, message_id: int, customer_id: int):
        updated_message: dict = await self.presenter.update_message(
            message_id=message_id,
            customer_id=customer_id,
            updated_data=UpdateMessageSchema(text=updated_text)
        )
        if not updated_message:
            return
        else:
            json_updated_message = MessageSchema(**updated_message).json()
            await self.websocket.send_json(data=json_updated_message)

    @staticmethod
    def save_message_to_elastic(message: dict):
        client = ElasticClient(hosts=get_settings().elastic_host).client
        es_service = MessageElasticService(client=client)
        es_service.save_message(
            _id=message['id'],
            text=message['text'],
            from_customer_id=message['from_customer_id'],
            to_customer_id=message['to_customer_id'],
            channel_id=message['channel_id']
        )

    async def write_message(
            self, text: str, sender_id: int, channel_id: int,
            receiver_id: int | None
    ):
        message: dict = await self.presenter.save_message(
            from_customer_id=sender_id,
            message_data=CreateMessageSchema(
                text=text, to_customer_id=receiver_id
            ),
            channel_id=channel_id
        )
        self.save_message_to_elastic(message=message)
        json_message = MessageSchema(**message).json()
        await self.websocket.send_json(data=json_message)

    async def user_typing(self, sender_username: str):
        data = {
            'username': sender_username,
            'message': 'username typing'
        }
        await self.websocket.send_json(data=data)

    async def check_handle(
            self, obj_data: dict, channel: dict, sender_customer):
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
                    text = obj_data.get('text')
                    receiver_id = obj_data.get('receiver_id')
                    await self.write_message(
                        channel_id=channel['id'],
                        text=text,
                        receiver_id=receiver_id,
                        sender_id=sender_customer.id
                    )
            case MessageType.USER_TYPING.value:
                await self.user_typing(sender_customer.username)
            case MessageType.UPDATE.value:
                updated_text = obj_data.get('text')
                message_id = obj_data.get('message_id')
                await self.update_message(
                    updated_text=updated_text,
                    message_id=message_id,
                    customer_id=sender_customer.id
                )
            case MessageType.READ.value:
                offset = obj_data.get('offset')
                limit = obj_data.get('limit')
                data = {
                    'channel_id': channel['id'],
                    'offset': offset,
                    'limit': limit
                }
                await self.read_message(**data)
