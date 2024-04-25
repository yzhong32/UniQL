import pymysql
from neo4j import GraphDatabase

# Database credentials
mysql_config = {
    'host': '127.0.0.1',
    'user': 'cs511',
    'password': 'cs511password',
    'database': 'device'
}

neo4j_config = {
    'uri': 'bolt://127.0.0.1:7687',
    'user': 'neo4j',
    'password': 'cs511password'
}

# Connect to MySQL
def connect_to_mysql(config):
    return pymysql.connect(**config)

# Connect to Neo4j
def connect_to_neo4j(config):
    driver = GraphDatabase.driver(config['uri'], auth=(config['user'], config['password']))
    return driver

# Fetch all tables from MySQL
def get_all_tables(connection):
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = [item[0] for item in cursor.fetchall()]
    cursor.close()
    return tables

# Fetch data in batches from a MySQL table
def fetch_data_in_batches(connection, table_name, batch_size=1000):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [desc[0] for desc in cursor.description]
    
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield columns, rows

# Batch insert nodes in Neo4j
def batch_insert_nodes(driver, table_name, columns, rows):
    with driver.session() as session:
        session.execute_write(create_nodes_transaction, table_name, columns, rows)
        print(f"Inserted a batch of {len(rows)} records into Neo4j for table {table_name}")

# Neo4j transaction function for node creation
def create_nodes_transaction(tx, table_name, columns, rows):
    for row in rows:
        properties = {columns[i]: row[i] for i in range(len(row))}
        cypher_query = f"CREATE (n:{table_name} {{ {', '.join(f'{key}: ${key}' for key in properties.keys())} }})"
        tx.run(cypher_query, **properties)

# Main function
def main():
    print("Starting the database migration...")
    mysql_conn = connect_to_mysql(mysql_config)
    neo4j_driver = connect_to_neo4j(neo4j_config)
    
    try:
        tables = get_all_tables(mysql_conn)
        print(f"Found {len(tables)} tables to migrate.")
        for table_name in tables:
            print(f"Processing table: {table_name}")
            for columns, rows in fetch_data_in_batches(mysql_conn, table_name):
                columns = [c.lower() for c in columns]
                # print(columns)
                batch_insert_nodes(neo4j_driver, table_name, columns, rows)
        print("Migration completed successfully.")
    except Exception as e:
        print(f"An error occurred during migration: {e}")
    finally:
        mysql_conn.close()
        neo4j_driver.close()
        print("Database connections closed.")

if __name__ == "__main__":
    main()