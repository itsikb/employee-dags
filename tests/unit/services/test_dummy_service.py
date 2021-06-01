from employee_dags.include.services.dummy_service import DummyService
from unittest.mock import MagicMock


class TestDummyService(object):

    def setup_method(self):
        self.__client = MagicMock()
        self.__dummy_service = DummyService(self.__client)

    def test_function(self):
        self.__dummy_service.do_something()
        self.__client.function.assert_called_once_with()
