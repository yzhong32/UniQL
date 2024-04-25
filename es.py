from elasticsearch import Elasticsearch, helpers


def get_elasticsearch_conn():
    es = Elasticsearch(hosts=['https://localhost:9200'], basic_auth=('cs511', 'cs511password'),
                       ca_certs='/home/ubuntu/elasticsearch-8.13.0/config/certs/http_ca.crt')
    return es

es = get_elasticsearch_conn()

database_name = "device"

converter_resp = {
    "inner_index": ["shop"],
    "query": {
        "bool": {
            "must": [
                {
                    "bool": {
                        "should": [
                            {
                                "range": {
                                    "Open_Year": {
                                        "gt": 2012
                                    }
                                }
                            },
                            {
                                "range": {
                                    "Open_Year": {
                                        "lt": 2008
                                    }
                                }
                            }
                        ],
                        "minimum_should_match": 1
                    }
                }
            ]
        }
    },
    "_source": ["Location"]
}
index = converter_resp.pop("inner_index")
formatted_index = "{db}_{table}".format(db=database_name, table=index[0])

mapping = es.indices.get_mapping(index="{db}_{table}".format(db=database_name, table=index[0]))
print("mapping:{}".format(mapping))
print("---------------------")

code = {}
if "code" in converter_resp:
    code = converter_resp.pop("code")

response = es.search(index=formatted_index, body=converter_resp)
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