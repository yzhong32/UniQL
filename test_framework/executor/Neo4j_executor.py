import json
from neo4j import GraphDatabase
from .base import QueryExecutor

class Neo4jExecutor(QueryExecutor):
    def __init__(self):
        self.driver = None

    def init(self, config_path):
        with open(config_path) as config_file:
            config = json.load(config_file)
        uri = config['uri']
        user = config['user']
        password = config['password']
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        if self.driver is not None:
            self.driver.close()

    def execute_query(self, query, database=None, schema=None):
        session = self.driver.session(database=database) if database else self.driver.session()
        try:
            print(str(query))
            query = str(query)
            results = session.run(query)
            formatted_results = []
            for record in results:
                if schema:
                    record_json = {field: record.get(field) for field in schema}
                else:
                    record_json = dict(record.items())
                formatted_results.append(json.dumps(record_json))
            return formatted_results, None
        except Exception as e:
            return None, e
        finally:
            session.close()

    def get_schema(self, label_name):
        query = f"""
            MATCH (n:{label_name})
            WITH n LIMIT 10
            UNWIND keys(n) AS key
            RETURN collect(distinct key) AS keys
            """
        session = self.driver.session()
        try:
            results = session.run(query).single()
            keys = results["keys"]
            return keys
        except Exception as e:
            print(f"Error retrieving schema for label {label_name}: {e}")
            return None
        finally:
            session.close()

    def __del__(self):
        self.close()

if __name__ == '__main__':
    executor = Neo4jExecutor()
    executor.init('../config/neo4j_config.json')
    label_name = 'swimmer'
    print(executor.get_schema(label_name))
