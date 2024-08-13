import json
import pandas as pd
from collections import defaultdict

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
# Toma un diccionario potencialmente anidado y lo aplana
def flatten_dict(d, parent_key='', sep='--'):
    items = []
    # Cada subclave se combina con su clave padre usando un separador (por defecto es "--")
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def create_translation_dataframe(es_data, en_data, fr_data):
    combined_dict = defaultdict(dict)
    all_keys = set(en_data.keys()).union(set(es_data.keys())).union(set(fr_data.keys()))

    for key in all_keys:
        en_value = en_data.get(key, "")
        es_value = es_data.get(key, "")
        fr_value = fr_data.get(key, "")
        
        # Se verifica si algún valor es un diccionario
        if isinstance(en_value, dict):
            en_value = flatten_dict(en_value, key)
        else:
            en_value = {key: en_value}
        
        if isinstance(es_value, dict):
            es_value = flatten_dict(es_value, key)
        else:
            es_value = {key: es_value}
        
        if isinstance(fr_value, dict):
            fr_value = flatten_dict(fr_value, key)
        else:
            fr_value = {key: fr_value}
        
        # Se asegura de que todas las subclaves se agreguen correctamente al combined_dict
        for sub_key in set(en_value.keys()).union(es_value.keys()).union(fr_value.keys()):
            combined_dict[sub_key]['Key'] = sub_key
            combined_dict[sub_key]['English'] = en_value.get(sub_key, "")
            combined_dict[sub_key]['Spanish'] = es_value.get(sub_key, "")
            combined_dict[sub_key]['French'] = fr_value.get(sub_key, "")

    df = pd.DataFrame.from_dict(combined_dict, orient='index')
    return df

def save_to_excel(df, file_path):
    df.to_excel(file_path, index=False)

def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def main():
    # File paths for the translation files
    es_file = 'es.json'
    en_file = 'en.json'
    fr_file = 'fr.json'

    # Load the translation data from JSON files
    es_data = load_json(es_file)
    en_data = load_json(en_file)
    fr_data = load_json(fr_file)

    # Create a DataFrame with the translations
    df = create_translation_dataframe(es_data, en_data, fr_data)

    # Save the DataFrame to an Excel file
    output_file = 'translations.xlsx'
    save_to_excel(df, output_file)
    print(f"Translations saved to {output_file}")

    # Save JSON files
    save_json(en_data, 'en-converted-JSON.json')
    save_json(es_data, 'es-converted-JSON.json')
    save_json(fr_data, 'fr-converted-JSON.json')

if __name__ == "__main__":
    main()
