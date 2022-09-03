from dataclasses import dataclass

from .interfaces.password_service_interface import PasswordServiceInterface
from passlib.context import CryptContext


@dataclass
class PasswordService(PasswordServiceInterface):
    context: CryptContext

    async def verify_password(
            self, plain_password: str,
            hashed_password: str
    ) -> bool:
        return self.context.verify(secret=plain_password, hash=hashed_password)

    async def hashed_password(self, password: str) -> str:
        return self.context.hash(secret=password)
