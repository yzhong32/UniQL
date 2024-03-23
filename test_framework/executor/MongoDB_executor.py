import json

from pymongo import MongoClient

from .base import SQLExecutor

class MongoDBExecutor(SQLExecutor):
    def __init__(self):
        self.client = None
        self.db = None

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
                results.append(json.dumps(doc_json))

            return results

        except Exception as e:
            return []
        
