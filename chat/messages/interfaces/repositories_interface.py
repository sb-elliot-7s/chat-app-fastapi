from abc import ABC, abstractmethod
from ..schemas import CreateMessageSchema, UpdateMessageSchema, \
    SearchMessageSchema
from .elastic_message_interface import MessageSearchElasticInterface


class MessageRepositoriesInterface(ABC):

    @abstractmethod
    async def save_message(
            self, from_customer_id: int, message_data: CreateMessageSchema,
            channel_id: int,
    ):
        pass

    @abstractmethod
    async def get_messages(
            self, channel_id: int, customer_id: int | None, limit: int,
            offset: int, is_chat: bool = True
    ):
        pass

    @abstractmethod
    async def get_message(self, message_id: int, customer_id: int):
        pass

    @abstractmethod
    async def delete_message(self, message_id: int, customer_id: int):
        pass

    @abstractmethod
    async def update_message(
            self, message_id: int, customer_id: int,
            updated_data: UpdateMessageSchema
    ):
        pass


class MessageSearchInterface(ABC):
    def search_messages(
            self, options: SearchMessageSchema,
            receiver: MessageSearchElasticInterface
    ):
        pass
