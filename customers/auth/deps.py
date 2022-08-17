from fastapi import Depends, status
from .schemas import TokenSchema
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db_session
from .repositories import CustomerRepositories
from .password_service import PasswordService
from .token_service import TokenService

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def get_option_presenter(session: AsyncSession = Depends(get_db_session)):
    yield {
        'repository': CustomerRepositories(session=session),
        'password_service': PasswordService(context=password_context),
        'token_service': TokenService()
    }


response_data = {
    'login': {
        'path': '/login',
        'status_code': status.HTTP_200_OK,
        'response_model': TokenSchema
    },
    'signup': {
        'path': '/signup',
        'status_code': status.HTTP_201_CREATED
    }
}
