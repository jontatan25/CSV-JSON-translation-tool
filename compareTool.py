import json
import os

def load_json(file_path):
    """Load a JSON file from the given path, handling JSONDecodeError."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error loading JSON file '{file_path}': {e}")
        raise
    except Exception as e:
        print(f"Unexpected error loading file '{file_path}': {e}")
        raise

def compare_json_keys(original, translated):
    """Compare keys between original and translated JSON objects."""
    original_keys = set(original.keys())
    translated_keys = set(translated.keys())
    
    missing_in_translated = original_keys - translated_keys
    missing_in_original = translated_keys - original_keys
    
    return missing_in_translated, missing_in_original

def generate_report(missing_in_translated, missing_in_original):
    """Generate report of missing keys."""
    report_lines = []
    
    if missing_in_translated:
        report_lines.append("Keys missing in the translated file:")
        for key in missing_in_translated:
            report_lines.append(f"  - {key}")
        report_lines.append(f"Total missing in translated file: {len(missing_in_translated)}")
    else:
        report_lines.append("No keys missing in the translated file.")
    
    if missing_in_original:
        report_lines.append("Keys missing in the original file:")
        for key in missing_in_original:
            report_lines.append(f"  - {key}")
        report_lines.append(f"Total missing in original file: {len(missing_in_original)}")
    else:
        report_lines.append("No keys missing in the original file.")
    
    return "\n".join(report_lines)

def main(original_file, translated_file, report_file):
    """Main function to compare JSON files and generate a report."""
    original = load_json(original_file)
    translated = load_json(translated_file)
    
    missing_in_translated, missing_in_original = compare_json_keys(original, translated)
    
    report = generate_report(missing_in_translated, missing_in_original)
    
    with open(report_file, 'w', encoding='utf-8') as file:
        file.write(report)
    
    print(f"Report generated: {report_file}")

if __name__ == "__main__":
    # Define the file paths for original and translated JSON files
    original_files = ['en.json', 'es.json', 'fr.json']
    translated_files = ['en-translated.json', 'es-translated.json', 'fr-translated.json']
    
    # Ensure that both lists have the same length
    if len(original_files) != len(translated_files):
        raise ValueError("The number of original files must match the number of translated files.")
    
    for orig, trans in zip(original_files, translated_files):
        report_file = f"report_{os.path.splitext(orig)[0]}.txt"
        try:
            main(orig, trans, report_file)
        except Exception as e:
            print(f"Failed to process files {orig} and {trans}: {e}")
