import os
# noinspection PyUnresolvedReferences
from mock.mock import patch
from pytest import raises, fixture

from employee_dags.conf import AppConfiguration


PRODUCTION = "production"
STAGING = "staging"
LOCAL = "default"
TEST = "test"


class TestConfig(object):
    @fixture(autouse=True)
    def test_environment(self):
        self.__patch_env(TEST)

    def test_config_should_load_value(self, test_environment):
        assert AppConfiguration.domain.key1 == 'value1'

    def test_config_should_load_value_by_string(self, test_environment):
        assert "value1" == AppConfiguration["domain"]["key1"]

    def test_raises_error_on_missing_root_node(self, test_environment):
        with raises(AttributeError):
            AppConfiguration.mynoval

    def test_raises_error_on_missing_nested_node(self, test_environment):
        with raises(AttributeError):
            AppConfiguration.domain.mynoval

    def test_raises_error_on_missing_root_node_by_string(self, test_environment):
        with raises(AttributeError):
            AppConfiguration['mynoval']

    def test_raises_error_on_missing_nested_node_by_string(self, test_environment):
        with raises(AttributeError):
            AppConfiguration["domain"]["mynoval"]

    def test_load_configuration_with_env_prod(self):
        self.__patch_env(PRODUCTION)

    def test_load_configuration_with_env_staging(self):
        self.__patch_env(STAGING)

    def test_load_configuration_with_env_local(self):
        self.__patch_env(LOCAL)

    def __patch_env(self, env):
        with patch.dict(os.environ, ENVIRONMENT_TYPE=env):
            AppConfiguration.reload()
