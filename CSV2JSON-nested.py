import json
import pandas as pd
from collections import defaultdict

def load_excel(file_path):
    return pd.read_excel(file_path)

def create_json_from_dataframe(df):
    en_data = {}
    es_data = {}
    fr_data = {}

    for _, row in df.iterrows():
        key = row['Key']

        # Handle keys with nested structures
        if '--' in key:
            base_key, sub_key = key.split('--', 1)

            # Ensure the base key is a dictionary; if not, create it
            if base_key not in en_data or not isinstance(en_data[base_key], dict):
                en_data[base_key] = {}
            if base_key not in es_data or not isinstance(es_data[base_key], dict):
                es_data[base_key] = {}
            if base_key not in fr_data or not isinstance(fr_data[base_key], dict):
                fr_data[base_key] = {}

            # Assign the nested key-value pairs, ensuring that existing data is not overwritten
            if pd.notna(row['English']):
                en_data[base_key][sub_key] = row['English']
            if pd.notna(row['Spanish']):
                es_data[base_key][sub_key] = row['Spanish']
            if pd.notna(row['French']):
                fr_data[base_key][sub_key] = row['French']
        else:
            if pd.notna(row['English']):
                en_data[key] = row['English']
            if pd.notna(row['Spanish']):
                es_data[key] = row['Spanish']
            if pd.notna(row['French']):
                fr_data[key] = row['French']

    return en_data, es_data, fr_data

def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def main():
    # Path to the Excel file
    excel_file = 'translations.xlsx'

    # Load the Excel data
    df = load_excel(excel_file)

    # Create JSON data from the DataFrame
    en_data, es_data, fr_data = create_json_from_dataframe(df)

    # Save the JSON data to files
    save_json(en_data, 'enJSON.json')
    save_json(es_data, 'esJSON.json')
    save_json(fr_data, 'frJSON.json')

    print("Translations saved to enJSON.json, esJSON.json, and frJSON.json")

if __name__ == "__main__":
    main()
