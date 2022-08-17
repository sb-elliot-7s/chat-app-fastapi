from dataclasses import dataclass
from .interfaces.repositories_interface import CustomerRepositoriesInterface
from .interfaces.password_service_interface import PasswordServiceInterface
from .interfaces.token_service_interface import TokenServiceInterface
from .exceptions import AuthExceptions


@dataclass
class CustomerPresenter:
    repository: CustomerRepositoriesInterface
    password_service: PasswordServiceInterface
    token_service: TokenServiceInterface

    async def __check(self, username: str, password: str):
        if not (customer := await self.repository.receive_customer_by_username(
                username=username)) or \
                not await self.password_service.verify_password(
                    plain_password=password,
                    hashed_password=customer.password):
            raise AuthExceptions().incorrect_username_or_password
        return customer

    async def login(self, username: str, password: str):
        customer = await self.__check(username=username, password=password)
        options = {'data': {'sub': customer.username}}
        token = await self.token_service.encode_token(**options)
        return {
            'access_token': token,
            'token_type': 'bearer'
        }

    async def sign_up(self, username: str, password: str):
        if await self.repository.receive_customer_by_username(username=username):
            raise AuthExceptions().username_exists
        _password = await self.password_service \
            .hashed_password(password=password)
        await self.repository.save_user(username=username, password=_password)
