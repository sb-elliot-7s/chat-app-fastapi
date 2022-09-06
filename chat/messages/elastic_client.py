from elasticsearch_dsl import Search, Document, Date, Boolean, Text, Integer
from functools import wraps

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.response import Response
from fastapi import HTTPException, status
from .interfaces.elastic_message_interface import MessageSearchElasticInterface
from .schemas import SearchMessageSchema


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


class MessageSearchElasticService(MessageSearchElasticInterface):
    def __init__(self, client, index: str = 'message'):
        self.index = index
        self.client = client

    def search(self, options: SearchMessageSchema) -> Response:
        searched = Search(using=self.client, index=self.index) \
            .query('match', text=options.text)
        if options.channel_id:
            searched = searched.filter('term', channel_id=options.channel_id)
        if options.from_date or options.to_date:
            searched = self.date_filter(
                from_date=options.from_date, to_date=options.to_date,
                searched=searched
            )
        return searched.execute()

    @staticmethod
    def range_date_filter(searched, filter_date):
        return searched.filter('range', **{'created': filter_date})

    def date_filter(self, from_date, to_date, searched):
        from_and_to_date = {
            'searched': searched,
            'filter_date': {'gte': from_date, 'lte': to_date}
        }
        to_date_ = {'searched': searched, 'filter_date': {'lte': to_date}}
        from_date_ = {'searched': searched, 'filter_date': {'gte': from_date}}
        return self.range_date_filter(
            **from_and_to_date) if from_date and to_date \
            else self.range_date_filter(**to_date_) if not from_date \
            else self.range_date_filter(**from_date_)


class MessageElasticService:

    def __init__(self, client):
        self.client = client

    @staticmethod
    def save_message(message_object: dict):
        message = MessageDocument(**message_object)
        message.meta.id = message_object.get('id')
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
