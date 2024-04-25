from test_framework.executor.MongoDB_executor import MongoDBExecutor


if __name__ == '__main__':
    executor = MongoDBExecutor()
    executor.init('/home/ubuntu/SQLLMConverter/test_framework/config/mongodb_config.json')
    database = 'swimming'
    table_name = 'swimmer'
    # print(executor.get_schema(database, table_name))
    # result = executor.execute_query('db.event.aggregate([{ "$group": { "_id": None, "count": { "$sum": 1 } } }])', database, {})

    result = executor.execute_query('db.trip.aggregate([{"$match": {"bike_id": 636}}, {"$group": {"_id": None, "totalDuration": {"$sum": "$duration"}, "maxDuration": {"$max": "$duration"}}}])', database, {})
    print(result)