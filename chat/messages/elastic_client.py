from elasticsearch_dsl import Search, Document, Date, Boolean, Text, Integer
from datetime import datetime
from functools import wraps

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.response import Response
from fastapi import HTTPException, status


def object_exist_or_none(object_data: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if (obj := func(*args, **kwargs)) is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'{object_data} not found'
                )
            return obj

        return wrapper

    return decorator


class ElasticClient:
    def __init__(self, hosts: str | list[str] = 'http://localhost:9200'):
        self.client = connections.create_connection(hosts=hosts)

    def create_the_index_and_populate_the_mappings(self, document: Document):
        document.init(using=self.client)


class MessageElasticService:

    def __init__(self, client, index: str = 'message'):
        self.client = client
        self.index = index

    def search(self, message_text: str):
        searched = Search(using=self.client, index=self.index) \
            .query('match', text=message_text)
        response: Response = searched.execute()
        return response

    @staticmethod
    def save_message(
            _id: int, text: str, from_customer_id: int,
            to_customer_id: int, channel_id: int
    ):
        message = MessageDocument(
            id=_id,
            text=text,
            from_customer_id=from_customer_id,
            to_customer_id=to_customer_id,
            channel_id=channel_id,
            read=False,
            is_active=True
        )
        message.meta.id = _id
        message.save()

    def delete_message(self, message_id: int):
        message = self.get_message(message_id=message_id)
        message.delete()

    def update_message(self, message_id: int, text: str):
        message = self.get_message(message_id=message_id)
        message.update(text=text, refresh=True)

    @staticmethod
    @object_exist_or_none(object_data='Message')
    def get_message(message_id: int):
        return MessageDocument.get(id=message_id, ignore=404)

    @staticmethod
    def get_messages(message_ids: list[int], missing: str):
        return MessageDocument.mget(
            docs=message_ids, raise_on_error=False, missing=missing)


class MessageDocument(Document):
    id = Integer()
    text = Text()
    from_customer_id = Integer()
    to_customer_id = Integer()
    channel_id = Integer()
    created = Date(default_timezone='UTC')
    updated = Date(default_timezone='UTC')
    read = Boolean()
    is_active = Boolean()

    class Index:
        name = 'message'

    def save(self, **kwargs):
        self.created = datetime.utcnow()
        self.updated = datetime.utcnow()
        return super().save(**kwargs)