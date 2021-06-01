from os import environ, getenv
import pkgutil

import re
import yaml


def _get_config_file_name():
    return environ.get("ENVIRONMENT_TYPE", "default") + ".yml"


def _load_configuration():
    CONFIG_NAME = _get_config_file_name()
    binary_data = pkgutil.get_data('employee_dags.conf', CONFIG_NAME)
    decoded_file = binary_data.decode('utf-8')
    return yaml.load(decoded_file)


def _replace_env_var(value):
    reg = re.compile(r'^<(.+?)>$')
    env_var = reg.search(str(value))
    return getenv(env_var.group(1)) if env_var else value


class ConfigBuilder(type):
    def __new__(meta, clsName, bases, attr):
        meta.__getitem__ = meta.get = meta.__getattr__
        cls = type.__new__(meta, clsName, bases, attr)
        cls.tree = _load_configuration()
        cls.config_file = _get_config_file_name()
        return cls

    def __getattr__(cls, name, *default):
        try:
            return ConfigData(cls.tree, ".".join(["ROOT", name]), cls.config_file).get(name)
        except:
            if default: return default[0]
            raise AttributeError('No such configuration {name}, config file is {config_file}'
                                 .format(name=name,
                                         config_file=cls.config_file))


class ConfigData:
    def __init__(self, root, path, config_file):
        self.__class__.__getitem__ = self.__class__.get = self.__class__.__getattr__
        self.root = root
        self.path = path
        self.config_file = config_file

    def __getattr__(self, name, *default):
        try:
            node = self.root[name]
            return _replace_env_var(node) if type(node) != dict \
                else ConfigData(node, ".".join([self.path, name]), self.config_file)
        except:
            if default: return default[0]
            raise AttributeError(
                'No such configuration {key} for path {path}, config file is {config_file}'
                    .format(key=name,
                            path=self.path,
                            config_file=self.config_file))


class AppConfiguration(metaclass=ConfigBuilder):
    @classmethod
    # for tests only
    def reload(cls):
        cls.tree = _load_configuration()
