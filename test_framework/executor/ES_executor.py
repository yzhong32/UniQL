from elasticsearch import Elasticsearch

# def get_elasticsearch_conn():
#     es = Elasticsearch(
#         hosts=['https://localhost:9200'], 
#         basic_auth=('cs511', 'cs511password'),
#         ca_certs='/home/ubuntu/elasticsearch-8.13.0/config/certs/http_ca.crt'
#     )
#     return es

# def simple_es_query(es, index_name, query):
#     response = es.search(index=index_name, body={"query": {"match_all": {}}})
#     return response

from .base import QueryExecutor  # Assuming there is a BaseExecutor to inherit from


class ElasticsearchExecutor(QueryExecutor):
    def __init__(self):
        self.client = self.get_elasticsearch_conn()
        self.index = None

    def get_elasticsearch_conn(self):
        # Set up the Elasticsearch connection using the provided details
        es = Elasticsearch(
            hosts=['https://localhost:9200'],
            basic_auth=('cs511', 'cs511password'),
            ca_certs='/home/ubuntu/elasticsearch-8.13.0/config/certs/http_ca.crt'
        )
        return es

    def execute_query(self, query, index, schema):
        self.index = index

        try:
            # Execute the query using the Elasticsearch search() method
            response = self.client.search(index=self.index, body=query)

            results = []
            for hit in response['hits']['hits']:
                # Convert each hit/document to match the desired schema
                doc_json = {field: hit['_source'].get(field, None) for field in schema}
                results.append(json.dumps(doc_json))

            return results, None

        except Exception as e:
            return None, e


import json

if __name__ == '__main__':
    # Create an instance of the ElasticsearchExecutor
    executor = ElasticsearchExecutor()

    # Define a test index name - replace 'your_index' with a real index from your Elasticsearch
    test_index = 'bike_1_weather'

    # Define a test query - this example matches all documents, but you should replace it with your actual query
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
        "_source": ["zip_code"]
    }

    # Define a schema for the documents you expect back - replace these fields with those relevant to your data
    test_schema = ['zip_code']

    # Execute the query
    results, error = executor.execute_query(test_query, test_index, test_schema)

    # Check if there was an error
    if error is not None:
        print(f"An error occurred: {error}")
    else:
        # Print the results
        print("Query results:")
        for doc in results:
            print(json.loads(doc))

# if __name__ == '__main__':
#     es = get_elasticsearch_conn()

#     # Define the index to query
#     index_name = 'bike_1_trip'

#     # Define a simple query. In this example, it retrieves all documents
#     query = es.search(index=index_name, body={"query": {"match_all": {}}})

#     # Execute the query
#     response = simple_es_query(es, index_name, query)

#     # Process and print out the results
#     for hit in response['hits']['hits']:
#         print(hit['_source'])
