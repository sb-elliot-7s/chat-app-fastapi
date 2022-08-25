from .interfaces.token_service_interface import TokenServiceInterface


class CreateTokenMixin:
    @staticmethod
    async def create_token(username: str, token_service: TokenServiceInterface):
        options = {'data': {'sub': username}}
        token = await token_service.encode_token(**options)
        return {
            'access_token': token,
            'token_type': 'bearer'
        }
