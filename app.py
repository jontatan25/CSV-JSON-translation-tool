import json
import pandas as pd
from collections import defaultdict

# define base path 
TRANSLATIONS_BASE_PATH = './'

# define translation files path
ES_FILE = TRANSLATIONS_BASE_PATH + '/es.json'
EN_FILE = TRANSLATIONS_BASE_PATH + '/en.json'
FR_FILE = TRANSLATIONS_BASE_PATH + '/fr.json'

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def create_translation_dataframe(es_data, en_data, fr_data):
    combined_dict = defaultdict(dict)
    all_keys = set(en_data.keys()).union(set(es_data.keys())).union(set(fr_data.keys()))

    for key in all_keys:
        combined_dict[key]['Key'] = key
        combined_dict[key]['English'] = en_data.get(key, None)
        combined_dict[key]['Spanish'] = es_data.get(key, key) if key in es_data else key
        combined_dict[key]['French'] = fr_data.get(key, None)

    df = pd.DataFrame.from_dict(combined_dict, orient='index')

    return df

def save_to_excel(df, file_path):
    df.to_excel(file_path, index=False)

def main():
    # Load the translation data from JSON files
    es_data = load_json(ES_FILE)
    en_data = load_json(EN_FILE)
    fr_data = load_json(FR_FILE)

    # Create a DataFrame with the translations
    df = create_translation_dataframe(es_data, en_data, fr_data)

    # Save the DataFrame to an Excel file
    output_file = 'translationsA.xlsx'
    save_to_excel(df, output_file)
    print(f"Translations saved to {output_file}")

if __name__ == "__main__":
    main()