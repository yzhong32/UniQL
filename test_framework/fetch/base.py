import json
from typing import List, Tuple


class QueryFetcher(object):
    def __init__(self):
        return

    def fetch_query(self, file_folder: str, file_name: str) -> List[Tuple[str, str]]:
        with open('{}/{}'.format(file_folder, file_name), 'r') as file:
            queries_info = json.load(file)

        queries = []
        for _, query_info in queries_info.items():
            queries.append((query_info['db_id'], query_info['query']))

        return queries
