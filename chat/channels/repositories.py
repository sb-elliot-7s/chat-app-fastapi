from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from sqlalchemy import select, insert, delete, update
from sqlalchemy.orm import subqueryload

from .schemas import CreateChannelSchema, UpdateChannelSchema
from .models import Channel, Subscribers
from .exceptions import ChannelExceptions
from .interfaces.repositories_interface import \
    ChannelRepositoriesInterface


@dataclass
class ChannelRepositories(ChannelRepositoriesInterface):
    session: AsyncSession

    async def get_channels(self, customer_id: int, limit: int, offset: int):
        channels_ids_query = select(Subscribers.channel_id) \
            .where(Subscribers.customer_id == customer_id) \
            .scalar_subquery()
        stmt = select(Channel) \
            .where(Channel.id.in_(channels_ids_query)) \
            .limit(limit) \
            .offset(offset) \
            .order_by(Channel.created.desc())
        result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def create_channel(
            self, customer_id: int, channel_data: CreateChannelSchema):
        stmt = insert(Channel).values(
            owner_id=customer_id,
            slug=channel_data.channel_name,
            **channel_data.dict()
        ).returning(Channel)
        result = await self.session.execute(statement=stmt)
        await self.session.commit()
        return result.first()

    async def delete_channel(self, customer_id: int, channel_slug: str):
        stmt = delete(Channel) \
            .where(Channel.owner_id == customer_id,
                   Channel.slug == channel_slug)
        result = await self.session.execute(statement=stmt)
        await self.session.commit()
        return result.rowcount

    async def update_channel(
            self, customer_id: int, channel_slug: str,
            updated_data: UpdateChannelSchema
    ):
        stmt = update(Channel) \
            .where(Channel.slug == channel_slug,
                   Channel.owner_id == customer_id).values(
            slug=updated_data.channel_name,
            **updated_data.dict(exclude_none=True)
        )
        _ = await self.session.execute(statement=stmt)
        await self.session.commit()

    async def get_channel(self, channel_slug: str):
        stmt = select(Channel) \
            .options(subqueryload(Channel.online_customers)) \
            .options(subqueryload(Channel.subscribers)) \
            .where(Channel.slug == channel_slug)
        result: AsyncResult = await self.session.execute(statement=stmt)
        return result.scalars().first()

    async def __check_channel(self, channel_slug: str):
        if not (channel := await self.get_channel(channel_slug=channel_slug)):
            raise ChannelExceptions().channel_not_found
        return channel

    async def subscribe(self, customer_id: int, channel_slug: str):
        channel = await self.__check_channel(channel_slug=channel_slug)
        subs_stmt = insert(Subscribers) \
            .values(customer_id=customer_id, channel_id=channel.id)
        _ = await self.session.execute(statement=subs_stmt)
        await self.session.commit()

    async def unsubscribe(self, customer_id: int, channel_id: int):
        channel_subs_stmt = delete(Subscribers).where(
            Subscribers.channel_id == channel_id,
            Subscribers.customer_id == customer_id
        )
        result = await self.session.execute(statement=channel_subs_stmt)
        await self.session.commit()
        return result.rowcount

    async def check_if_user_in_subscribed(
            self, customer_id: int, channel_id: int):
        exists_stmt = select(Subscribers.id) \
            .select_from(Channel) \
            .join(Subscribers, Channel.id == Subscribers.channel_id) \
            .where(Subscribers.channel_id == channel_id,
                   Subscribers.customer_id == customer_id)
        result: AsyncResult = await self.session.execute(statement=exists_stmt)
        return True if result.scalars().first() else False
