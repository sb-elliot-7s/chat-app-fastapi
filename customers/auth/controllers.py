from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from .schemas import CreateCustomerSchema, BaseCustomerAccountSchema
from .presenter import CustomerPresenter, TokenPresenter
from .deps import get_option_presenter, response_data, get_token_service_data

auth_controllers = APIRouter(prefix='/auth', tags=['customers'])


@auth_controllers.post(**response_data.get('signup'))
async def sign_up(
        customer_data: CreateCustomerSchema,
        option_presenter=Depends(get_option_presenter),
):
    return await CustomerPresenter(**option_presenter) \
        .sign_up(**customer_data.dict())


@auth_controllers.post(**response_data.get('login'))
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        option_presenter=Depends(get_option_presenter),
):
    return await CustomerPresenter(**option_presenter) \
        .login(username=form_data.username, password=form_data.password)


@auth_controllers.post(**response_data.get('create_token'))
async def get_token(username: BaseCustomerAccountSchema,
                    token_data=Depends(get_token_service_data)):
    return await TokenPresenter(**token_data).get_token(username=username.username)
