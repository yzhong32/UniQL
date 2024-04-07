from elasticsearch import Elasticsearch

def get_elasticsearch_conn():
    es = Elasticsearch(
        hosts=['https://localhost:9200'], 
        basic_auth=('cs511', 'cs511password'),
        ca_certs='/home/ubuntu/elasticsearch-8.13.0/config/certs/http_ca.crt'
    )
    return es

def simple_es_query(es, index_name, query):
    response = es.search(index=index_name, body={"query": {"match_all": {}}})
    return response

if __name__ == '__main__':
    es = get_elasticsearch_conn()
    
    # Define the index to query
    index_name = 'bike_1_trip'
    
    # Define a simple query. In this example, it retrieves all documents
    query = es.search(index=index_name, body={"query": {"match_all": {}}})
    
    # Execute the query
    response = simple_es_query(es, index_name, query)
    
    # Process and print out the results
    for hit in response['hits']['hits']:
        print(hit['_source'])
