from datetime import datetime

from pydantic import BaseModel, Field


class CreateChannelSchema(BaseModel):
    channel_name: str = Field(max_length=200)
    describe_info: str | None = Field(None, max_length=255)


class UpdateChannelSchema(BaseModel):
    channel_name: str | None = Field(None, max_length=200)
    describe_info: str | None = Field(None, max_length=255)


class ChannelSchema(CreateChannelSchema):
    id: int
    owner_id: int
    created: datetime

    online_customers: list
    messages: list

    class Config:
        orm_mode = True


class MessageImage(BaseModel):
    id: int
    photo_url: str
    message_id: int
    created: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda d: d.strftime('%Y-%m-%d %H:%M')
        }


class UpdateMessageSchema(BaseModel):
    text: str


class CreateMessageSchema(UpdateMessageSchema):
    text: str
    to_customer_id: int | None


class MessageSchema(CreateMessageSchema):
    id: int
    created: datetime
    from_customer_id: int
    read: bool = False
    is_active: bool = True

    images: list[MessageImage] | None

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda d: d.strftime('%Y-%m-%d %H:%M')
        }
