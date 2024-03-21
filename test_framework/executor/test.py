if __name__ == "__main__":
    from MongoDB_executor import MongoDBExecutor
    from MySQL_executor import MySQLExecutor

    # For MySQL
    mysql_executor = MySQLExecutor()
    mysql_executor.init('../config/mysql_config.json')
    result = mysql_executor.execute_query('SELECT * FROM weather LIMIT 10', 'bike_1')
    print(result)

    # For MongoDB
    mongodb_executor = MongoDBExecutor()
    mongodb_executor.init('../config/mongodb_config.json')
    result = mongodb_executor.execute_query("{\"collection\": \"weather\", \"find\": {}, \"limit\": 10}", "admin")
    print(result)