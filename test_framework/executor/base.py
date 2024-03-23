import abc
import json
import os


class SQLExecutor(abc.ABC):
    @abc.abstractmethod
    def init(self, config_path):
        pass

    @abc.abstractmethod
    def execute_query(self, query, database, schema):
        pass
