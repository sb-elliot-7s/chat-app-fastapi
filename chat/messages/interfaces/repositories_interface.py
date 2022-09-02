from abc import ABC, abstractmethod
from ..schemas import CreateMessageSchema, UpdateMessageSchema


class MessageRepositoriesInterface(ABC):

    @abstractmethod
    async def save_message(
            self, from_customer_id: int,
            message_data: CreateMessageSchema,
            channel_id: int,
    ):
        pass

    @abstractmethod
    async def get_messages(
            self, channel_id: int, customer_id: int | None, limit: int,
            offset: int
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
