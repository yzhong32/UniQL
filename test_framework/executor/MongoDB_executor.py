import json

from pymongo import MongoClient

from base import SQLExecutor

class MongoDBExecutor(SQLExecutor):
    def __init__(self):
        self.client = None
        self.db = None

    def init(self, config_path):
        with open(config_path) as config_file:
            config = json.load(config_file)
        self.client = MongoClient(config['host'], config.get('port', 27017))

    def execute_query(self, query, database, schema):
        json_object = json.loads(query)
        self.db = self.client[database]
        collection = self.db[json_object['collection']]
        
        if 'limit' in json_object:
            result_cursor = collection.find(json_object['find']).limit(json_object['limit'])
        else:
            result_cursor = collection.find(json_object['find'])
        
        results = []
        for doc in result_cursor:
            doc_json = {field: doc.get(field, None) for field in schema}
            results.append(json.dumps(doc_json))
        
        return results
