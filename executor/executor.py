import abc
import json
import os

class SQLExecutor(abc.ABC):
    @abc.abstractmethod
    def init(self, config_path):
        pass

    @abc.abstractmethod
    def execute_query(self, query, database):
        pass


if __name__ == "__main__":
    from MongoDB_executor import MongoDBExecutor
    from MySQL_executor import MySQLExecutor

    # For MySQL
    mysql_executor = MySQLExecutor()
    mysql_executor.init('./executor/mysql_config.json')
    result = mysql_executor.execute_query('SELECT * FROM weather', 'bike_1')
    print(result)

    # For MongoDB
    mongodb_executor = MongoDBExecutor()
    mongodb_executor.init('./executor/mongodb_config.json')
    result = mongodb_executor.execute_query("{\"collection\": \"weather\", \"find\": {}}", "admin")
    print(result)