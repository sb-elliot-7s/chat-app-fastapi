from fastapi import status
from .schemas import MessageSchema
from database import get_db_session
from .presenter import MessagePresenter, MessageSearchPresenter
from fastapi import Depends
from .repositories import MessageRepositories, MessageSearchRepository
from .elastic_client import MessageSearchElasticService, ElasticClient
from settings import get_settings

response_data = {
    'search': {
        'path': '/search',
        'status_code': status.HTTP_200_OK,
    },
    'my_messages_from_channels': {
        'path': '/',
        'status_code': status.HTTP_200_OK,
        'response_model': list[MessageSchema]
    },
    'delete_message': {
        'path': '/{message_id}',
        'status_code': status.HTTP_204_NO_CONTENT
    },
    'get_message': {
        'path': '/{message_id}',
        'status_code': status.HTTP_200_OK,
        'response_model': MessageSchema
    },
    'update': {
        'path': '/{message_id}',
        'status_code': status.HTTP_200_OK,
        'response_model': MessageSchema
    },
    'ws_chat': {
        'path': '/ws/{channel_slug}'
    }
}


async def get_presenter(session=Depends(get_db_session)):
    presenter = MessagePresenter(MessageRepositories(session=session))
    yield presenter


def get_message_search_presenter() -> MessageSearchPresenter:
    repository = MessageSearchRepository()
    return MessageSearchPresenter(search_repository=repository)


def get_message_elastic_service():
    es_client = ElasticClient(hosts=get_settings().elastic_host).client
    receiver = MessageSearchElasticService(client=es_client)
    yield receiver
