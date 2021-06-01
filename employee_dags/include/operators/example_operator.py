from airflow.models import BaseOperator, SkipMixin
from airflow.utils.decorators import apply_defaults

from employee_dags.include.client.dummy_client import DummyClient
from employee_dags.include.services.dummy_service import DummyService


class ExampleOperator(BaseOperator, SkipMixin):
    """
        This is example operator.
    """

    ui_color = '#fde0f0'

    @apply_defaults
    def __init__(
            self,
            *args, **kwargs):

        super().__init__(*args, **kwargs)

        dummy_client = DummyClient()
        self.__dummy_service = DummyService(dummy_client)

    def execute(self, context):

        self.log.info('Doing some logging')
        tmp_var = self.__dummy_service.do_something()
        self.log.info("result: {tmp_var}".format(tmp_var=tmp_var))

        self.log.info('Done.')