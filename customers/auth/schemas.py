from pydantic import BaseModel, Field


class BaseCustomerAccountSchema(BaseModel):
    username: str = Field(max_length=200)


class CreateCustomerSchema(BaseCustomerAccountSchema):
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
