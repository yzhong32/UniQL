from elasticsearch import Elasticsearch, helpers


def get_elasticsearch_conn():
    es = Elasticsearch(hosts=['https://localhost:9200'], basic_auth=('cs511', 'cs511password'),
                       ca_certs='/home/ubuntu/elasticsearch-8.13.0/config/certs/http_ca.crt')
    return es

es = get_elasticsearch_conn()

query = {
  "size": 0,
  "aggs": {
    "group_by_city": {
      "terms": {
        "field": "city.keyword"
      },
      "aggs": {
        "max_latitude": {
          "max": {
            "field": "lat"
          }
        }
      }
    }
  }
}

response = es.search(index="bike_1_station", body=query)

for bucket in response['aggregations']['group_by_city']['buckets']:
    print(f"City: {bucket['key']}, Max Latitude: {bucket['max_latitude']['value']}")