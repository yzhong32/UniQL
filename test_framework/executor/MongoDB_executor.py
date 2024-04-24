import json
import simplejson

from pymongo import MongoClient

from .base import QueryExecutor

class MongoDBExecutor(QueryExecutor):
    def __init__(self):
        self.client = None
        self.db = None

    def get_schema(self, database, table_name):
        self.db = self.client[database]
        collection = self.db[table_name]
        documents = collection.aggregate([{'$sample': {'size': 10}}])
        schema = set()
        for doc in documents:
            schema.update(doc.keys())

        return ', '.join(schema)


    def init(self, config_path):
        with open(config_path) as config_file:
            config = json.load(config_file)
        self.client = MongoClient(config['host'], config.get('port', 27017))

    def execute_query(self, query, database, schema):
        self.db = self.client[database]
        
        exec_env = {
            "db": self.db,
        }

        try:
            adjusted_query = f'result = {query}'
            exec(adjusted_query, exec_env)
            records = exec_env.get("result")

            results = []
            for doc in records:
                doc_json = {field: doc.get(field, None) for field in schema}
                results.append(simplejson.dumps(doc_json))

            return results, None

        except Exception as e:
            return None, e

if __name__ == '__main__':
    executor = MongoDBExecutor()
    executor.init('../config/mongodb_config.json')
    database = 'swimming'
    table_name = 'swimmer'
    print(executor.get_schema(database, table_name))
