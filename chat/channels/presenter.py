from dataclasses import dataclass
from .channel_schemas import UpdateChannelSchema, CreateChannelSchema
from .interfaces.channel_repositories_interface import \
    ChannelRepositoriesInterface
from .exceptions import ChannelExceptions


@dataclass
class ChannelPresenter:
    repository: ChannelRepositoriesInterface

    async def get_channels(self, customer_id: int, limit: int, offset: int):
        return await self.repository \
            .get_channels(customer_id=customer_id, limit=limit, offset=offset)

    async def create_channel(
            self, customer_id: int, channel_data: CreateChannelSchema
    ):
        return await self.repository \
            .create_channel(customer_id=customer_id, channel_data=channel_data)

    async def delete_channel(self, customer_id: int, channel_slug: str):
        result = await self.repository \
            .delete_channel(customer_id=customer_id, channel_slug=channel_slug)
        if not result:
            raise ChannelExceptions().channel_not_found

    async def update_channel(
            self, customer_id: int, channel_slug: str,
            updated_data: UpdateChannelSchema
    ):
        return await self.repository \
            .update_channel(customer_id=customer_id, channel_slug=channel_slug,
                            updated_data=updated_data)

    async def get_channel(self, channel_slug: str):
        result = await self.repository.get_channel(channel_slug=channel_slug)
        if result is None:
            raise ChannelExceptions().channel_not_found
        return result

    async def subscribe(self, customer_id: int, channel_slug: str):
        return await self.repository \
            .subscribe(customer_id=customer_id, channel_slug=channel_slug)

    async def unsubscribe(self, customer_id: int, channel_id: int):
        result = await self.repository \
            .unsubscribe(customer_id=customer_id, channel_id=channel_id)
        if not result:
            raise ChannelExceptions()\
                .unsubscribe(customer_id=customer_id, channel_id=channel_id)
