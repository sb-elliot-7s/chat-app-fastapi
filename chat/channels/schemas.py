from pydantic import BaseModel, Field
from datetime import datetime

from customers.profile.schemas import CustomerSchema


class CreateChannelSchema(BaseModel):
    channel_name: str = Field(max_length=200)
    describe_info: str | None = Field(None, max_length=255)


class UpdateChannelSchema(BaseModel):
    channel_name: str | None = Field(None, max_length=200)
    describe_info: str | None = Field(None, max_length=255)

    @property
    def is_empty(self): return not self.dict(exclude_none=True)


class ChannelSchema(CreateChannelSchema):
    id: int
    owner_id: int
    slug: str | None
    created: datetime

    online_customers: list[CustomerSchema]
    subscribers: list[CustomerSchema]

    class Config:
        orm_mode = True
