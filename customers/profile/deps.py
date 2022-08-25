from .repositories import ProfileRepositories
from fastapi import Depends, status
from database import get_db_session
from permissions import CustomerPermission
from ..auth.token_service import TokenService
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import CustomerSchema


async def get_presenter(session: AsyncSession = Depends(get_db_session)):
    yield {
        'repositories': ProfileRepositories(session=session)
    }


async def get_customer_data(
        customer=Depends(CustomerPermission(token_service=TokenService())
                         .get_current_user)
):
    yield customer


response_data = {
    'add_image': {
        'path': '/images/{image_name}',
        'status_code': status.HTTP_201_CREATED
    },
    'delete_image': {
        'path': '/images/{image_name}',
        'status_code': status.HTTP_204_NO_CONTENT
    },
    'get_customer': {
        'path': '/',
        'status_code': status.HTTP_200_OK,
        'response_model': CustomerSchema
    },
    'update_customer': {
        'path': '/',
        'status_code': status.HTTP_200_OK,
    },
    'delete_customer': {
        'path': '/',
        'status_code': status.HTTP_204_NO_CONTENT
    }
}
