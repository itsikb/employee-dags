from employee_dags.include.client.dummy_client import DummyClient


class TestDummyClient(object):

    def setup_method(self):
        self._dummy_client = DummyClient()

    def test_function(self):
        expected_result = 1
        actual_result = self._dummy_client.function()

        assert actual_result == expected_result
