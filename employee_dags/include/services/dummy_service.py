import logging

logger = logging.getLogger(__name__)


class DummyService:
    def __init__(self, client):
        self.__client = client

    def do_something(self):
        return self.__client.function()
