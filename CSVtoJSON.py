import json
import pandas as pd

def load_excel(file_path):
    return pd.read_excel(file_path)

def create_json_from_dataframe(df):
    en_data = {}
    es_data = {}
    fr_data = {}

    for _, row in df.iterrows():
        key = row['Key']

        # Directly assign values without handling nested keys
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
    save_json(en_data, 'en-translated.json')
    save_json(es_data, 'es-translated.json')
    save_json(fr_data, 'fr-translated.json')

    print("Translations saved to en-translated.json, es-translated.json, and fr-translated.json")

if __name__ == "__main__":
    main()
