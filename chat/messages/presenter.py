from dataclasses import dataclass

from .interfaces.repositories_interface import MessageRepositoriesInterface, \
    MessageSearchInterface
from .schemas import CreateMessageSchema, UpdateMessageSchema, \
    SearchMessageSchema
from .exceptions import MessageExceptions
from .interfaces.elastic_message_interface import MessageSearchElasticInterface


@dataclass
class MessagePresenter:
    repository: MessageRepositoriesInterface

    async def save_message(
            self, from_customer_id: int,
            message_data: CreateMessageSchema,
            channel_id: int,
    ):
        return await self.repository.save_message(
            from_customer_id=from_customer_id, message_data=message_data,
            channel_id=channel_id
        )

    async def get_messages(
            self, channel_id: int, customer_id: int | None, limit: int,
            offset: int, is_chat: bool = True
    ):
        return await self.repository.get_messages(
            channel_id=channel_id, customer_id=customer_id, limit=limit,
            offset=offset, is_chat=is_chat
        )

    async def get_message(self, message_id: int, customer_id: int):
        return await self.repository.get_message(
            message_id=message_id, customer_id=customer_id)

    async def delete_message(self, message_id: int, customer_id: int):
        if not (result := await self.repository.delete_message(
                message_id=message_id, customer_id=customer_id
        )):
            raise MessageExceptions().message_not_found

    async def update_message(
            self, message_id: int, customer_id: int,
            updated_data: UpdateMessageSchema
    ):
        return await self.repository.update_message(
            message_id=message_id,
            customer_id=customer_id,
            updated_data=updated_data
        )


@dataclass
class MessageSearchPresenter:
    search_repository: MessageSearchInterface

    def search_messages(
            self, options: SearchMessageSchema,
            receiver: MessageSearchElasticInterface,
    ):
        return self.search_repository.search_messages(
            options=options, receiver=receiver)
