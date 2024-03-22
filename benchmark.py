import csv
from executor.MongoDB_executor import MongoDBExecutor
from executor.MySQL_executor import MySQLExecutor


def process_sql_queries(file_path, executor_base, converter_executor_pairs):
    results = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            table, query = row['table'], row['query']
            is_successful = []
            base = executor_base(query, table)
            for converter, executor in converter_executor_pairs:
                converted_query = converter(table, query)
                execution_result = executor(converted_query, table)
                is_successful.append(base == execution_result)
            results.append(is_successful)

        return results


def converter_mongo(table, query):
    # if table == '3':
    #     return '1'
    return "{\"collection\": \"weather\", \"find\": {}}"


mysql_executor = MySQLExecutor()
mysql_executor.init('./test_framework/config/mysql_config.json')
mysql_executor = mysql_executor.execute_query

mongodb_executor = MongoDBExecutor()
mongodb_executor.init('./test_framework/config/mongodb_config.json')
mongodb_executor = mongodb_executor.execute_query

converter_executor_pairs = [(converter_mongo, mongodb_executor)]

file_path = './data.csv'
res = process_sql_queries(file_path, mysql_executor, converter_executor_pairs)

print(res)
