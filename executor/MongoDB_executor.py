import json
from pymongo import MongoClient

from .executor import SQLExecutor

class MongoDBExecutor(SQLExecutor):
    def __init__(self):
        self.client = None
        self.db = None

    def init(self, config_path):
        with open(config_path) as config_file:
            config = json.load(config_file)
        self.client = MongoClient(config['host'], config.get('port', 27017))

    def execute_query(self, query, database):
        # Assuming 'query' is a dictionary containing the collection name and actual query
        json_object = json.loads(query)
        
        self.db = self.client[database]
        collection = self.db[json_object['collection']]
        result = collection.find(json_object['find'])
        return str(list(result))
    

