import json
import pymysql

from base import SQLExecutor

# this is not an implementation of Executor
class MySQLExecutor(SQLExecutor):
    def __init__(self):
        self.connection = None

    def init(self, config_path):
        with open(config_path) as config_file:
            self.config = json.load(config_file)
            

    def execute_query(self, query, database, schema):
        if self.connection is None or self.connection.db != database:
            self.connection = pymysql.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                database=database
            )
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            field_names = [desc[0] for desc in cursor.description]
            results = []
            for row in result:
                row_json = {field: row[field_names.index(field)] for field in schema if field in field_names}
                results.append(json.dumps(row_json))
            return results

        
    def load_schema(self, query, database):
        if self.connection == None or self.connection.db != database:
            self.connection = pymysql.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                database=database
            )
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            field_names = [i[0] for i in cursor.description]
            return field_names