from pydantic import BaseModel, Field


class BaseCustomerAccountSchema(BaseModel):
    username: str | None = Field(max_length=200)


class CreateCustomerSchema(BaseCustomerAccountSchema):
    password: str


class TokenSchema(BaseModel):
    token: str
