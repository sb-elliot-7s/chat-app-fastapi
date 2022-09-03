from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from sqlalchemy import select, insert, delete, update
from .schemas import CreateMessageSchema, UpdateMessageSchema
from .models import Message

from .interfaces.repositories_interface import \
    MessageRepositoriesInterface


@dataclass
class MessageRepositories(MessageRepositoriesInterface):
    session: AsyncSession

    async def save_message(
            self, from_customer_id: int,
            message_data: CreateMessageSchema,
            channel_id: int,
    ):
        options = {
            'channel_id': channel_id,
            'from_customer_id': from_customer_id,
            **message_data.dict(exclude_none=True)
        }
        stmt = insert(Message).values(**options).returning(Message)
        result: AsyncResult = await self.session.execute(statement=stmt)
        await self.session.commit()
        return result.mappings().first()

    async def get_messages(
            self, channel_id: int, customer_id: int | None, limit: int,
            offset: int
    ):
        stmt = select(Message)
        if customer_id:
            stmt = stmt.where(Message.from_customer_id == customer_id)
        stmt = stmt \
            .where(Message.channel_id == channel_id) \
            .limit(limit) \
            .offset(offset) \
            .order_by(Message.updated.desc())
        result: AsyncResult = await self.session.execute(statement=stmt)
        return result.scalars().unique().all()

    async def get_message(self, message_id: int, customer_id: int):
        stmt = select(Message).where(Message.id == message_id)
        result: AsyncResult = await self.session.execute(statement=stmt)
        return result.scalars().first()

    async def delete_message(self, message_id: int, customer_id: int):
        stmt = delete(Message).where(
            Message.id == message_id,
            Message.from_customer_id == customer_id
        )
        result = await self.session.execute(statement=stmt)
        await self.session.commit()
        return result.rowcount

    async def update_message(
            self, message_id: int, customer_id: int,
            updated_data: UpdateMessageSchema
    ):
        stmt = update(Message) \
            .where(Message.id == message_id,
                   Message.from_customer_id == customer_id) \
            .values(**updated_data.dict()) \
            .returning(Message)
        result: AsyncResult = await self.session.execute(statement=stmt)
        await self.session.commit()
        return result.first()
