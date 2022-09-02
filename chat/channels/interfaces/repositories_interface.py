from abc import ABC, abstractmethod
from ..schemas import CreateChannelSchema, UpdateChannelSchema


class ChannelRepositoriesInterface(ABC):
    @abstractmethod
    async def get_channels(self, customer_id: int, limit: int, offset: int):
        pass

    @abstractmethod
    async def create_channel(
            self, customer_id: int, channel_data: CreateChannelSchema
    ):
        pass

    @abstractmethod
    async def delete_channel(self, customer_id: int, channel_slug: str):
        pass

    async def update_channel(
            self, customer_id: int, channel_slug: str,
            updated_data: UpdateChannelSchema
    ):
        pass

    @abstractmethod
    async def get_channel(self, channel_slug: str):
        pass

    @abstractmethod
    async def subscribe(self, customer_id: int, channel_slug: str):
        pass

    @abstractmethod
    async def unsubscribe(self, customer_id: int, channel_id: int):
        pass
