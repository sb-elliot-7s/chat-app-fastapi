from abc import ABC, abstractmethod


class TokenServiceInterface(ABC):

    @abstractmethod
    async def encode_token(self, data: dict) -> str:
        pass

    @abstractmethod
    async def decode_token(self, token: str) -> dict:
        pass
