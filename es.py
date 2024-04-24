from elasticsearch import Elasticsearch, helpers


def get_elasticsearch_conn():
    es = Elasticsearch(hosts=['https://localhost:9200'], basic_auth=('cs511', 'cs511password'),
                       ca_certs='/home/ubuntu/elasticsearch-8.13.0/config/certs/http_ca.crt')
    return es

es = get_elasticsearch_conn()

database_name = "bike_1"

converter_resp = {
  "size": 0,
  "aggs": {
    "zip_codes": {
      "terms": {
        "field": "zip_code",
        "size": 1,
        "order": {
          "avg_pressure": "asc"
        }
      },
      "aggs": {
        "avg_pressure": {
          "avg": {
            "field": "mean_sea_level_pressure_inches.keyword"
          }
        }
      }
    }
  },
  "inner_index": ["weather"],
  "code": {
    "zip_code": "response['aggregations']['zip_codes']['buckets'][0]['key']"
  }
}





index = converter_resp.pop("inner_index")

code = {}
if "code" in converter_resp:
    code = converter_resp.pop("code")

response = es.search(index="{db}_{table}".format(db=database_name, table=index[0]), body=converter_resp)
print(response)
print("---------------------")

exec_result_dict = {'response':response}
for k,v in code.items():
    try:
        exec('{} = {}'.format(k, v), globals(), exec_result_dict)
    except Exception as e:
        continue
exec_result_dict.pop('response')
print('exec_result_dict:', exec_result_dict)