from elasticsearch import Elasticsearch
import json

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

from test_framework.executor.base import QueryExecutor  # Assuming there is a BaseExecutor to inherit from
import simplejson


class ElasticsearchExecutor(QueryExecutor):
    def __init__(self):
        self.client = self.get_elasticsearch_conn()
        self.index = None

    def get_elasticsearch_conn(self):
        # Set up the Elasticsearch connection using the provided details
        es = Elasticsearch(
            hosts=['https://127.0.0.1:9200'],
            basic_auth=('cs511', 'cs511password'),
            ca_certs='/home/ubuntu/elasticsearch-8.13.0/config/certs/http_ca.crt'
        )
        return es

    def get_schema(self, index_name):
        try:
            mappings = self.client.indices.get_mapping(index=index_name)
            properties = mappings[index_name]['mappings']['properties']
            schema = {}
            for field, details in properties.items():
                schema[field] = details.get('type', 'unknown')  # 'unknown' as default if type is not specified

            return schema

        except Exception as e:
            print(f"Error retrieving schema for index {index_name}: {e}")
            return None

    def init(self, config_path):
        pass

    def execute_query(self, inpt, database, schema):
        try:
            query = simplejson.loads(str(inpt))
            table = query.pop("inner_index")
            if "size" not in query:
                query["size"] = 10000
            print("**************************************************")
            print(query)
            print("**************************************************")
            self.index = database+'_'+table[0]

            code = {}
            if "code" in query:
                code = query.pop('code')

        except Exception as e:
            return None, e

        try:
            # Execute the query using the Elasticsearch search() method
            response = self.client.search(index=self.index, body=query)

            results = []
            for hit in response['hits']['hits']:
                # Convert each hit/document to match the desired schema
                doc_json = {field: hit['_source'].get(field, None) for field in schema}
                results.append(json.dumps(doc_json))
            
            exec_result_dict = {'response':response}
            for k,v in code.items():
                try:
                    exec('{}={}'.format(k, v), None, exec_result_dict)
                except Exception as e:
                    continue
            exec_result_dict.pop('response')
            print('exec_result_dict:', exec_result_dict)

            return results, None

        except Exception as e:
            return None, e

    def get_schema(self, index_name):
        try:
            mappings = self.client.indices.get_mapping(index=index_name)
            properties = mappings[index_name]['mappings']['properties']
            field_names = list(properties.keys())
            return field_names

        except Exception as e:
            print(f"Error retrieving schema for index {index_name}: {e}")
            return None
        
    def get_schemas(self, database, table_list):
        # Initialize an empty string to store the concatenated schema
        concatenated_schema = ""

        # Loop through each table name in the list
        for table in table_list:
            schema = self.get_schema(table)
            if schema is not None:
                if concatenated_schema:  # Add the table name as a splitter if it's not the first schema
                    concatenated_schema += f"{table}: {schema}\n"
                else:
                    concatenated_schema = schema  # Start with the first schema without a splitter
            else:
                print(f"No schema found for {table}. Skipping.")

        return concatenated_schema
        


if __name__ == '__main__':
    executor = ElasticsearchExecutor()
    index_name = 'bike_1_trip'
    schema = executor.get_schema(index_name)
    print(schema)

# if __name__ == '__main__':
#    # Create an instance of the ElasticsearchExecutor
#    executor = ElasticsearchExecutor()

#    # Define a test index name - replace 'your_index' with a real index from your Elasticsearch
#    database = 'bike_1'

#    # Define a test query - this example matches all documents, but you should replace it with your actual query
#    # SQL: SELECT zip_code FROM weather WHERE mean_visibility_miles  <  10
#    test_query = {
#        "query": {
#            "bool": {
#                "filter": [
#                    {
#                        "range": {
#                            "mean_visibility_miles": {
#                                "lt": 10
#                            }
#                        }
#                    }
#                ]
#            }
#        },
#        "_source": ["zip_code"],
#        "inner_index": "weather"
#    }
#
#    # Define a schema for the documents you expect back - replace these fields with those relevant to your data
#    test_schema = ['zip_code']
#
#    # Execute the query
#    results, error = executor.execute_query(test_query, database, test_schema)
#
#    # Check if there was an error
#    if error is not None:
#        print(f"An error occurred: {error}")
#    else:
#        # Print the results
#        print("Query results:")
#        for doc in results:
#            print(json.loads(doc))

# if __name__ == '__main__':
#     es = get_elasticsearch_conn()
#
#     # Define the index to query
#     index_name = 'bike_1_trip'
#
#     # Define a simple query. In this example, it retrieves all documents
#     query = es.search(index=index_name, body={"query": {"match_all": {}}})
#
#     # Execute the query
#     response = simple_es_query(es, index_name, query)
#
#     # Process and print out the results
#     for hit in response['hits']['hits']:
#         print(hit['_source'])
