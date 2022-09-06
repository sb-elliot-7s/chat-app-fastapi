from abc import ABC, abstractmethod
from elasticsearch_dsl.response import Response
from ..schemas import SearchMessageSchema


class MessageSearchElasticInterface(ABC):

    @abstractmethod
    def search(self, options: SearchMessageSchema) -> Response: pass
