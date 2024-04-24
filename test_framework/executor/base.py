import abc


class QueryExecutor(abc.ABC):
    @abc.abstractmethod
    def init(self, config_path):
        pass

    @abc.abstractmethod
    def execute_query(self, query, database, schema):
        pass
    
    @abc.abstractmethod
    def get_schemas(self, database, table_list):
        pass
