import asyncio
from test_framework.executor.MySQL_executor import *
from test_framework.executor.MongoDB_executor import *
from test_framework.fetch.base import *
from test_framework.comparator.hash import *
from converter.convert import QueryConverter
from contextlib import redirect_stdout, redirect_stderr


async def benchmark():
    mysql_executor = MySQLExecutor()
    mysql_executor.init('./test_framework/config/mysql_config.json')

    mongodb_executor = MongoDBExecutor()
    mongodb_executor.init('./test_framework/config/mongodb_config.json')

    convertor = QueryConverter("./converter/plugins")
    query_fetcher = QueryFetcher()
    comparator = HashComparator()

    executed = set()
    count = 0
    success = 0

    with open('benchmark.log', 'w') as f:
        with redirect_stdout(f), redirect_stderr(f):
            for (database, query) in query_fetcher.fetch_query("./query", "bike_1.json"):
            # for (database, query) in [('bike_1', 'SELECT * FROM station WHERE city  =  "San Jose"')]:
                if query in executed:
                    continue
                executed.add(query)
                count += 1

                print(f"**********************SQL Query: {query}**************************")
                schema = mysql_executor.load_schema(query, database)
                print(schema)

                mysql_result, e = mysql_executor.execute_query(query, database, schema)
                if e is not None:
                    print('execute mysql query error:{}'.format(e))
                    continue

                mongo_query = await convertor.convert(query)
                print(f"**********************MongoDB Query: {mongo_query}**************************")

                mongo_result, e = mongodb_executor.execute_query(mongo_query, database, schema)
                if e is not None:
                    print('execute mongo query error:{}'.format(e))
                    continue

                matched_row, unmatched_row, e = comparator.compare(mysql_result, mongo_result)
                if unmatched_row == None or len(unmatched_row) != 0:
                    print(query)
                    print(e)
                    print("mysql res:", mysql_result)
                    print("mongo res:", mongo_result)


                if e is not None:
                    print("Error comparing: {}".format(e))
                    continue

                print('Matched: {}'.format(matched_row))
                print('Unmatched: {}'.format(unmatched_row))

                if len(unmatched_row) == 0:
                    success += 1
        
            print('Success: {}'.format(success))
            print('Total: {}'.format(count))


if __name__ == '__main__':
    asyncio.run(benchmark())
