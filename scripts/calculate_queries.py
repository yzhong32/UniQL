import json
import pandas as pd

def write_queries_to_excel(json_file_paths, excel_file_path):
    all_queries = []  # List to store queries from all files

    # Loop through each file path in the list
    for file_path in json_file_paths:
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Extract queries from the current file and add them to the list
            all_queries.extend([entry['query'] for entry in data.values()])

    # Create a DataFrame from the list of queries
    df = pd.DataFrame(all_queries, columns=['Query'])
    
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

    excel_file_path = 'output_queries_2.xlsx'  # The output Excel file name

    # Call the function with the list of JSON files
    write_queries_to_excel(json_file_paths, excel_file_path)
