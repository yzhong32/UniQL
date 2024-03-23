import pymysql

from MySQL_executor import MySQLExecutor
from MongoDB_executor import MongoDBExecutor

if __name__ == '__main__':
    mysql_executor = MySQLExecutor()
    mysql_executor.init('../config/mysql_config.json')

    schema = mysql_executor.load_schema('SELECT * FROM weather LIMIT 10', 'bike_1')

    mysql_result = mysql_executor.execute_query('SELECT * FROM weather', 'bike_1', schema)

    mongodb_executor = MongoDBExecutor()
    mongodb_executor.init('../config/mongodb_config.json')
    mongo_result = mongodb_executor.execute_query("{\"collection\": \"weather\", \"find\": {}}", "bike_1", schema)

    mysql_hash = set((idx, hash(row)) for idx, row in enumerate(mysql_result))
    mongo_hash = set((idx, hash(row)) for idx, row in enumerate(mongo_result))


    if len(mysql_hash) != len(mongo_hash):
        print("row number mismatch")
        exit(1)

    matched_row = []
    unmatched_row = []
    for idx, hash_value in mysql_hash:
        if (idx, hash_value) in mongo_hash:
            matched_row.append(idx)
        else:
            unmatched_row.append(idx)
            print("hash value not found for index:{idx} in mysql result ".format(idx=idx))


    print(sorted(matched_row))
    print(sorted(unmatched_row))
