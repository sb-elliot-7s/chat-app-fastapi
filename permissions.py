from dataclasses import dataclass

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult

from customers.auth.interfaces.token_service_interface import TokenServiceInterface
from settings import get_settings
from database import get_db_session
from fastapi import Depends, HTTPException, status
from sqlalchemy import select

from customers.auth.models import Customers


class PermissionException:
    username_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Username not found'
    )
    user_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='User not found'
    )


@dataclass
class CustomerPermission:
    OAUTH_TOKEN = OAuth2PasswordBearer(tokenUrl='/auth/login')

    token_service: TokenServiceInterface
    configs = get_settings()

    async def get_current_user(
            self, token: str = Depends(OAUTH_TOKEN),
            db: AsyncSession = Depends(get_db_session)
    ):
        payload: dict = await self.token_service.decode_token(token=token)
        if not (username := payload.get('sub')):
            raise PermissionException().username_not_found
        stmt = select(Customers) \
            .where(Customers.username == username, Customers.is_active)
        result: AsyncResult = await db.execute(statement=stmt)
        if not (user := result.scalars().first()):
            raise PermissionException().user_not_found
        return user
