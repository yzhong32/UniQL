from test_framework.fetch.base import QueryFetcher
from test_framework.executor.MongoDB_executor import MongoDBExecutor
from test_framework.executor.MySQL_executor import MySQLExecutor
from test_framework.comparator.hash import HashComparator
if __name__ == '__main__':
    sql_query = 'SELECT avg(lat) ,  avg(longitude) FROM station WHERE city  =  "San Jose"'
    mongo_query = 'db.station.aggregate([ { $match: { city: "San Jose" } }, { $group: { _id: null, avgLongitude: { $avg: "$longitude" } } }] )'

    mysql_executor = MySQLExecutor()
    mysql_executor.init('./test_framework/config/mysql_config.json')

    schema = mysql_executor.load_schema(sql_query, 'bike_1')

    mysql_result = mysql_executor.execute_query(sql_query, 'bike_1', schema)

    mongodb_executor = MongoDBExecutor()
    mongodb_executor.init('./test_framework/config/mongodb_config.json')
    mongo_result, e = mongodb_executor.execute_query(mongo_query, "bike_1", schema)
    print(e)
    print(mysql_result)
    print(mongo_result)

    print(HashComparator().compare(mysql_result, mongo_result))