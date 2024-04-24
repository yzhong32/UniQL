import json
import pymysql
import simplejson
from .base import QueryExecutor
from .utils import *


# this is not an implementation of Executor
class MySQLExecutor(QueryExecutor):
    def __init__(self):
        self.connection = None

    def init(self, config_path):
        with open(config_path) as config_file:
            self.config = json.load(config_file)
    
    def get_conn(self, database):
        self.connection = pymysql.connect(
            host=self.config['host'],
            user=self.config['user'],
            password=self.config['password'],
            database=database
        )

    def execute_query(self, query, database, schema):
        try:
            if self.connection is None or self.connection.db != database:
                self.get_conn(database)
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                field_names = [format_sql_field(desc[0]) for desc in cursor.description]
                results = []
                for row in result:
                    row_json = {field: row[field_names.index(field)] for field in schema if field in field_names}
                    results.append(simplejson.dumps(row_json))
                return results, None
        except Exception as e:
            return None, e

    def load_schema(self, query, database):
        try:
            if self.connection == None or self.connection.db != database:
                self.get_conn(database)
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                field_names = [format_sql_field(i[0]) for i in cursor.description]
                return field_names
        except Exception as e:
            return None, e

    def get_schema(self, database, table_name):
        try:
            if self.connection is None or self.connection.db != database:
                self.get_conn(database)

            query = f"""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s;
            """

            with self.connection.cursor() as cursor:
                cursor.execute(query, (database, table_name))
                results = cursor.fetchall()

            schema = [column_name[0] for column_name in results]
            return schema
        except Exception as e:
            print(f"Error retrieving schema: {e}")
            return None


if __name__ == '__main__':
    executor = MySQLExecutor()
    executor.init('../config/mysql_config.json')
    database = 'bike_1'
    table_name = 'weather'
    print(executor.get_schema(database, table_name))