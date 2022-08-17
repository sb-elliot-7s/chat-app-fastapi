from jose import jwt, JWTError
from dataclasses import dataclass
from .exceptions import AuthExceptions
from settings import get_settings

from .interfaces.token_service_interface import TokenServiceInterface


def decode_token_decorator(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            raise AuthExceptions().token_exception
        except JWTError:
            raise AuthExceptions().credentials_exception

    return wrapper


@dataclass
class TokenService(TokenServiceInterface):
    CONFIGS = get_settings()

    async def encode_token(self, data: dict) -> str:
        payload = data.copy()
        payload.update({'exp': self.CONFIGS.access_token_expire_minutes})
        __data = {
            'claims': payload,
            'key': self.CONFIGS.secret_key,
            'algorithm': self.CONFIGS.algorithm
        }
        return jwt.encode(**__data)

    @decode_token_decorator
    async def decode_token(self, token: str) -> dict:
        __data = {
            'token': token,
            'key': self.CONFIGS.secret_key,
            'algorithms': self.CONFIGS.algorithm
        }
        return jwt.decode(**__data)
