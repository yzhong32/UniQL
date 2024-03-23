import asyncio
from test_framework.executor.MySQL_executor import * 
from test_framework.executor.MongoDB_executor import * 
from test_framework.fetch.base import * 
from test_framework.comparator.hash import * 
from converter.convert import QueryConverter

async def benchmark():
    mysql_executor = MySQLExecutor()
    mysql_executor.init('./test_framework/config/mysql_config.json')

    mongodb_executor = MongoDBExecutor()
    mongodb_executor.init('./test_framework/config/mongodb_config.json')

    convertor = QueryConverter("./converter/plugins")
    query_fetcher = QueryFetcher()
    comparator = HashComparator()

    for (database, query) in query_fetcher.fetch_query("./query", "bike_1.json"):
        print(f"**********************SQL Query: {query}**************************")
        schema = mysql_executor.load_schema(query, database)

        mysql_result = mysql_executor.execute_query(query, database, schema)

        mongo_query = await convertor.convert(query)
        # mongo_query = 'db.weather.find({ "max_humidity": { "$gte": 90 } },{ "max_humidity": 1, "_id": 0 }).limit(10)'
        print(f"**********************MongoDB Query: {mongo_query}**************************")
        mongo_result = mongodb_executor.execute_query(mongo_query, database, schema)

        matched_row, unmatched_row, e = comparator.compare(mysql_result, mongo_result)

        if e is not None:
            print("Error comparing: {}".format(e))
            continue

        print('Matched: {}'.format(matched_row))
        print('Unmatched: {}'.format(unmatched_row))

        print()
        print()

if __name__ == '__main__':
    asyncio.run(benchmark())

