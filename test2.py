import simplejson

query = """
{
    "size": 1000,
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
}"""

q = simplejson.loads(query)
print(q)
if "size" not in q:
    print("no size")
