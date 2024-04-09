test_query = {
    "query": {
        "bool": {
        "filter": [
            {
            "range": {
                "mean_visibility_miles": {
                "lt": 10
                }
            }
            }
        ]
        }
    },
    "_source": ["zip_code"],
    "inner_index": "weather"
}

inner_index = test_query.pop("inner_index")
print(inner_index)
print(test_query)