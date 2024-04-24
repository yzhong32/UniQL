import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML
import re

def extract_tables(sql_query):
    # Regular expression to find table names
    regex = r'\bFROM\b\s+([\w\.]+)|\bJOIN\b\s+([\w\.]+)'
    
    # Find all occurrences of table names
    matches = re.findall(regex, sql_query, re.IGNORECASE)
    
    # The matches list contains tuples, because of the groups in regex
    # Each tuple has one None, depending on whether FROM or JOIN matched
    # We use a set to avoid duplicates
    tables = set()
    for match in matches:
        tables.update([m for m in match if m])  # Add non-None matched table names to the set
    
    return list(tables)

# # 你的SQL语句
# sql = "SELECT avg(T1.lat) ,  avg(T1.longitude) FROM station AS T1 JOIN trip AS T2 ON T1.id  =  T2.start_station_id"
# tables_involved = extract_tables(sql)

# print("Tables involved in the SQL query:", tables_involved)

if __name__ == '__main__':
    test_queries = {
        "Simple Select": ("SELECT * FROM users;", ['users']),
        "Multiple Joins": ("SELECT * FROM users u JOIN orders o ON u.id = o.user_id JOIN products p ON o.product_id = p.id;", ['users', 'orders', 'products']),
        "Subquery in SELECT": ("SELECT (SELECT name FROM departments) AS dept_name FROM employees;", ['departments', 'employees']),
        "Subquery in FROM Clause": ("SELECT * FROM (SELECT * FROM orders) AS o;", ['orders']),
        "Subquery in JOIN Condition": ("SELECT * FROM employees e JOIN departments d ON e.department_id = (SELECT department_id FROM managers WHERE manager_id = e.manager_id);", ['employees', 'departments', 'managers']),
        "Complex Query with Multiple Subqueries": ("SELECT e.name, d.name FROM employees e JOIN departments d ON e.department_id = d.id WHERE exists (SELECT 1 FROM salaries s WHERE s.employee_id = e.id AND s.amount > 50000);", ['employees', 'departments', 'salaries']),
        "Use of WITH Clause": ("WITH RegionalSales AS (SELECT region, SUM(sales) AS total_sales FROM orders GROUP BY region) SELECT * FROM RegionalSales;", ['orders']),
        "Multiple Tables in FROM Clause": ("SELECT * FROM employees, departments;", ['employees', 'departments'])
    }

    for test_name, (query, expected) in test_queries.items():
        result = extract_tables(query)
        print(f"{test_name}: {'Pass' if result == expected else 'Fail'} - Expected {expected}, Got {result}")

