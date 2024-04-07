import json
from datetime import datetime

import pymysql
from elasticsearch import Elasticsearch, helpers

mysql_config_path = './test_framework/config/mysql_config.json'
mysql_database_name = 'bike_1'


def get_mysql_conn(database_name):
    with open(mysql_config_path) as config_file:
        config = json.load(config_file)
    conn = pymysql.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=database_name
    )
    return conn


def get_elasticsearch_conn():
    es = Elasticsearch(hosts=['https://localhost:9200'], basic_auth=('cs511', 'cs511password'),
                       ca_certs='/home/ubuntu/elasticsearch-8.13.0/config/certs/http_ca.crt')
    return es


def get_es_index_name(database_name, table_name):
    return database_name + '_' + table_name


def process_datetime_fields(row):
    for key, value in row.items():
        if isinstance(value, datetime):
            row[key] = value.isoformat()
    return row


def migrate_es():
    # get es and mysql conn
    mysql = get_mysql_conn(mysql_database_name)
    mysql_cursor = mysql.cursor()

    es = get_elasticsearch_conn()

    # find all tables under a db
    mysql_cursor.execute("SHOW TABLES;")
    tables = []
    for (table_name,) in mysql_cursor:
        tables.append(table_name)
    print("Tables in the database:", tables)

    for table in tables:
        print('-------------------------Migrating table:{}-------------------------------'.format(table))

        # fetch all data of a mysql table
        mysql_cursor.execute("SELECT * FROM {table};".format(table=table))
        all_rows = mysql_cursor.fetchall()
        mysql_total_row = len(all_rows)
        print("Total mysql rows:", mysql_total_row)

        # obtain schme
        mysql_cursor.execute("DESCRIBE {table}".format(table=table))
        columns = mysql_cursor.fetchall()
        column_names = [col[0] for col in columns]

        # convert rows tuple to dict
        all_rows_as_dicts = []
        for row in all_rows:
            row_dict = dict(zip(column_names, row))
            all_rows_as_dicts.append(row_dict)

        es_mapping = {
            "mappings": {
                "properties": {}
            }
        }

        type_mapping = {
            "int": "integer",
            "varchar": "text",
            "datetime": "date",
            # 添加其他需要的MySQL到Elasticsearch的数据类型映射
        }

        for column in columns:
            col_name = column[0]
            col_type = column[1].split("(")[0]  # 简化处理，不考虑长度等属性
            es_type = type_mapping.get(col_type, "text")  # 默认使用text
            es_mapping["mappings"]["properties"][col_name] = {"type": es_type}

        target_es_index_name = get_es_index_name(mysql_database_name, table)
        if es.indices.exists(index=target_es_index_name):
            es.indices.delete(index=target_es_index_name)
        else:
            es.indices.create(index=target_es_index_name, body=es_mapping)

        print("Migrating to es index:{}".format(target_es_index_name))

        print(es_mapping)

        # write into es index
        def generate_data(rows):
            for row in rows:
                yield {
                    '_index': target_es_index_name,
                    '_source': row,
                }

        try:
            helpers.bulk(es, generate_data(all_rows_as_dicts))
        except helpers.BulkIndexError as e:
            print('ES erros:', e.errors)
        except Exception as e:
            print('Exception:', e)

        es.indices.refresh(index=target_es_index_name)

        es_total_rows = es.count(index=target_es_index_name)['count']
        print("Total es rows:", es_total_rows)


if __name__ == '__main__':
    migrate_es()

