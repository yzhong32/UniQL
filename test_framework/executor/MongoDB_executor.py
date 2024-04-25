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
    
    def get_schemas(self, database, table_list):
        # Initialize an empty string to store the concatenated schema
        concatenated_schema = ""

        # Loop through each table name in the list
        for table in table_list:
            schema = self.get_schema(database, table)
            if schema is not None:
                if concatenated_schema:  # Add the table name as a splitter if it's not the first schema
                    concatenated_schema += f"{table}: {schema}\n"
                else:
                    concatenated_schema = schema  # Start with the first schema without a splitter
            else:
                print(f"No schema found for {table}. Skipping.")

        return concatenated_schema


    def init(self, config_path):
        with open(config_path) as config_file:
            config = json.load(config_file)
        self.client = MongoClient(config['host'], config.get('port', 27017))

    def execute_query(self, query, database, schema):
        print("here we are in executor, and the query is: ", query)
        self.db = self.client[database]
        
        exec_env = {
            "db": self.db,
        }

        try:
            adjusted_query = f'result = {query}'
            exec(adjusted_query, exec_env)
            records = exec_env.get("result")

            results = []
            origin_results = []
            for doc in records:
                doc_json = {field: doc.get(field, None) for field in schema}
                results.append(simplejson.dumps(doc_json))
                origin_results.append(simplejson.dumps(doc))

            print("result of mongodb:", origin_results)
            return results, None

        except Exception as e:
            return None, e

if __name__ == '__main__':
    executor = MongoDBExecutor()
    executor.init('/home/ubuntu/SQLLMConverter/test_framework/config/mongodb_config.json')
    database = 'swimming'
    table_name = 'swimmer'
    # print(executor.get_schema(database, table_name))
    # result = executor.execute_query('db.event.aggregate([{ "$group": { "_id": None, "count": { "$sum": 1 } } }])', database, {})

    result = executor.execute_query('db.station.aggregate([{ "$match": { "city": "San Jose" } }, { "$group": { "_id": None, "avgLatitude": { "$avg": "$lat" }, "avgLongitude": { "$avg": "$longitude" } }}])', database, {})
    print(result)
