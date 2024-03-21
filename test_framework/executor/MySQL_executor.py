import json
import pymysql

from base import SQLExecutor

class MySQLExecutor(SQLExecutor):
    def __init__(self):
        self.connection = None

    def init(self, config_path):
        with open(config_path) as config_file:
            self.config = json.load(config_file)
            

    def execute_query(self, query, database):
        if self.connection == None or self.connection.db != database:
            self.connection = pymysql.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                database=database
            )
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return str(result)
