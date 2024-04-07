from test_framework.fetch.base import QueryFetcher
from test_framework.executor.MongoDB_executor import MongoDBExecutor
from test_framework.executor.MySQL_executor import MySQLExecutor
from test_framework.executor.Neo4j_executor import Neo4jExecutor
from test_framework.comparator.hash import HashComparator

if __name__ == '__main__':
    sql_query = 'SELECT zip_code FROM weather GROUP BY zip_code HAVING avg(mean_visibility_miles)  <  10'
    mongo_query = 'db.station.aggregate([ { $match: { city: "San Jose" } }, { $group: { _id: null, avgLongitude: { $avg: "$longitude" } } }] )'
    # neo4j_query = '''
    # MATCH (s:Station {city: "San Jose"}) RETURN avg(s.longitude) AS averageLongit
    # '''
    # neo4j_query = '''
    # MATCH (w:Weather)
    #          WITH w.zipCode AS zip_code, AVG(w.meanVisibilityMiles) AS avgVisibility
    #          WHERE avgVisibility < 10
    #          RETURN zip_code;
    # '''

    neo4j_query = '''
    MATCH (w:Weather)
    WITH w.zip_code AS zip_code, AVG(w.mean_visibility_miles) AS avgVisibility
    WHERE avgVisibility < 10
    RETURN zip_code
    '''

    mysql_executor = MySQLExecutor()
    mysql_executor.init('./test_framework/config/mysql_config.json')

    schema = mysql_executor.load_schema(sql_query, 'bike_1')

    mysql_result, e = mysql_executor.execute_query(sql_query, 'bike_1', schema)

    mongodb_executor = MongoDBExecutor()
    mongodb_executor.init('./test_framework/config/mongodb_config.json')
    mongo_result, e = mongodb_executor.execute_query(mongo_query, "bike_1", ['avgLongitude'])

    neo4j_executor = Neo4jExecutor()
    neo4j_executor.init('./test_framework/config/neo4j_config.json')
    neo4j_result, e = neo4j_executor.execute_query(neo4j_query)


    print(e)
    print(mysql_result)
    # print(mongo_result)
    print(neo4j_result)

    # print(HashComparator().compare(mysql_result, mongo_result))
    print(HashComparator().compare(mysql_result, neo4j_result))