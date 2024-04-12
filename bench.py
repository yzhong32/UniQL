import argparse
import asyncio
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime
from enum import Enum
from typing import Tuple

from converter.convert import QueryConverter
from converter.memory import Memorier
from test_framework.comparator.hash import *
from test_framework.executor.ES_executor import ElasticsearchExecutor
from test_framework.executor.Neo4j_executor import Neo4jExecutor
from test_framework.executor.MongoDB_executor import MongoDBExecutor
from test_framework.executor.MySQL_executor import MySQLExecutor
from test_framework.executor.base import QueryExecutor
from test_framework.fetch.base import QueryFetcher


class DBName(Enum):
    MySQL = "mysql"
    MongoDB = "mongodb"
    Elasticsearch = "ES"
    Neo4j = "neo4j"


executor_get_func = {
    DBName.MySQL: MySQLExecutor,
    DBName.MongoDB: MongoDBExecutor,
    DBName.Elasticsearch: ElasticsearchExecutor,
    DBName.Neo4j: Neo4jExecutor
}


def get_bench_id(input_file: str, db_name: str) -> str:
    current_time = datetime.now()
    return 'benchmark-{target}-{input}-{time}'.format(target=db_name, input=input_file,
                                                      time=current_time.strftime("%Y-%m-%d#%H:%M:%S"))


def get_output_file_path(input_file: str, db_name: str) -> str:
    return './logs/{id}.log'.format(id=get_bench_id(input_file, db_name))


def get_memory_source(db_name: str) -> str:
    return './converter/memory/{db_name}'.format(db_name=db_name)


def get_database_executor(target: DBName) -> (QueryExecutor, QueryExecutor, Exception):
    config_file_folder = './test_framework/config/'
    # obtain mysql executor
    mysql_executor = MySQLExecutor()
    try:
        mysql_executor.init('{}/{}_config.json'.format(config_file_folder, DBName.MySQL.value))
    except Exception as e:
        return None, None, e

    # obtain target db executor
    if target not in executor_get_func:
        return None, None, Exception("Unsupported target database {}".format(target))

    get_func = executor_get_func[target]
    target_executor = get_func()
    # warning: we need to keep the config file name same as enum name
    try:
        target_executor.init('{}/{}_config.json'.format(config_file_folder, target.value))
    except Exception as e:
        return None, None, e

    return mysql_executor, target_executor, None


async def single_benchmark(mysql_executor: MySQLExecutor, target_executor: QueryExecutor,
                           converter: QueryConverter, comparator: QueryComparator, target_db: DBName,
                           queries: List[Tuple[str, str]],
                           use_memory: bool, memorier: Memorier):
    executed_queries = set()
    valid_query_count = 0
    success_query_count = 0
    idx = 1

    for (database, sql_query) in queries:
        # filter duplicate query
        if sql_query in executed_queries:
            continue
        executed_queries.add(sql_query)

        print()
        print("--------------------------{}-----------------".format(idx))
        idx += 1

        # get result schema
        schema = mysql_executor.load_schema(sql_query, database)
        print('schema:{}'.format(schema))

        print("---------------------------Execute SQL Query:{}-----------------".format(sql_query))
        # execute original SQL query in MySQL
        mysql_result, e = mysql_executor.execute_query(sql_query, database, schema)
        if e is not None:
            print('execute mysql query error:{}'.format(e))
            continue
        valid_query_count += 1

        # execute target query
        if use_memory:
            question = "Please convert the following SQL query to {db} query:\n {sql_query}".format(db=target_db.value,
                                                                                                    sql_query=sql_query)
            knowledge = await memorier.search_memory_examples(question)
            print("knowledge:{}".format(knowledge))
            target_query = await converter.convert_with_knowledge(sql_query, target_db.value, knowledge)
        else:
            target_query = await converter.convert(sql_query, target_db.value)

        print("---------------------------Execute Target Query:{}-----------------".format(target_query)) 
        if target_db.value == "neo4j":
            target_result, e = target_executor.execute_query(target_query)
        else:
            target_result, e = target_executor.execute_query(target_query, database, schema)

        if e is not None:
            print('execute target query error:{}'.format(e))
            continue

        match, unmatched_row, e = comparator.compare(mysql_result, target_result)
        if e is not None:
            print("Exception raised during comparison: {}".format(e))
            print("mysql res:", mysql_result)
            print("target res:", target_result)
            continue
        if not match:
            print("mismatch between MySQL and target")
            print("mysql res:", mysql_result)
            print("target res:", target_result)
        else:
            print('translate {q} success'.format(q=sql_query))
            success_query_count += 1

    print('success_query_count:', success_query_count)
    print('valid_count:', valid_query_count)
    print('accuracy:', success_query_count / valid_query_count)

async def benchmark(input_file: str, target_db: DBName, use_memory: bool):
    mysql_executor, target_executor, exception = get_database_executor(target_db)
    if exception is not None:
        print("Exception occurred in executor init: {}".format(exception))

    if use_memory:
        convertor = QueryConverter("./converter/plugins")
    else:
        convertor = QueryConverter("./converter/with_memory_plugins")

    query_fetcher = QueryFetcher()
    comparator = HashComparator()
    memorier = Memorier()

    queries = query_fetcher.fetch_query("./query", input_file)
    output_file_path = get_output_file_path(input_file, target_db.value)
    with open(output_file_path, 'w') as f:
        with redirect_stdout(f), redirect_stderr(f):
            if use_memory:
                await memorier.populate_memory(get_memory_source(target_db.value))
            print("--------")
            await single_benchmark(mysql_executor, target_executor, convertor, comparator, target_db, queries,
                                   use_memory, memorier)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Benchmark the converter')

    arg_parser.add_argument('-i', '--input', type=str,
                            help='file name that includes queries to be tested. Assume all files stored in ./query '
                                 'folder for now',
                            required=True)
    arg_parser.add_argument('-t', '--target', type=str, help='target database name', required=True)
    arg_parser.add_argument('-m', '--memory', type=bool, help='whether to use memory', required=True)

    args = arg_parser.parse_args()
    asyncio.run(benchmark(args.input, DBName(args.target), use_memory=args.use_memory))
