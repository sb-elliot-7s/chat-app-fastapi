from datetime import datetime

from pydantic import BaseModel


class MessageImageSchema(BaseModel):
    id: int
    photo_url: str
    message_id: int
    created: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda d: d.strftime('%Y-%m-%d %H:%M')
        }


class SearchMessageSchema(BaseModel):
    text: str


class UpdateMessageSchema(SearchMessageSchema):
    text: str


class CreateMessageSchema(UpdateMessageSchema):
    text: str
    to_customer_id: int | None


class MessageSchema(CreateMessageSchema):
    id: int
    channel_id: int
    created: datetime
    updated: datetime
    from_customer_id: int
    read: bool = False
    is_active: bool = True

    images: list[MessageImageSchema] | None

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda d: d.strftime('%Y-%m-%d %H:%M')
        }

    @classmethod
    def from_orm_to_json(cls, model_obj):
        return cls.from_orm(obj=model_obj).json()
