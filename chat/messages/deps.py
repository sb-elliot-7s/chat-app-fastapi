from fastapi import status
from .schemas import MessageSchema

response_data = {
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
