import json
import pandas as pd

def write_queries_to_excel(json_file_paths, excel_file_path):
    all_data = []  # List to store the data from all files

    # Helper function to check for JOINs in a query
    def has_join(query):
        return 1 if 'JOIN' in query.upper() else 0

    # Helper function to check for GROUP BY in a query
    def has_group_by(query):
        return 1 if 'GROUP BY' in query.upper() else 0

    # Loop through each file path in the list
    for file_path in json_file_paths:
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Extract details from the current file and add them to the list
            for entry in data.values():
                all_data.append({
                    'db_id': entry['db_id'],
                    'query': entry['query'],
                    'join?': has_join(entry['query']),
                    'aggregation?': has_group_by(entry['query'])
                })

    # Create a DataFrame from the list of data
    df = pd.DataFrame(all_data, columns=['db_id', 'query', 'join?', 'aggregation?'])
    
    # Write to Excel
    df.to_excel(excel_file_path, index=False, sheet_name='Queries')

if __name__ == "__main__":
    # List of JSON file paths
    json_file_paths = [
        './query/swimming.json',
        './query/railway.json',
        './query/allergy_1.json',
        './query/twitter_1.json',
        './query/small_bank_1.json',
        './query/scientist_1.json',
        './query/icfp_1.json',
        './query/wedding.json',
        './query/debate.json',
        './query/device.json',
    ]

    excel_file_path = 'output_queries_3.xlsx'  # The output Excel file name

    # Call the function with the list of JSON files
    write_queries_to_excel(json_file_paths, excel_file_path)
