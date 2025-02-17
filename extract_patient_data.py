import re
import json
import os
from pathlib import Path

# Define regex patterns
regex_name = re.compile(
    r"(?P<name>[A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+)+),\s*geb\.\s*am\s*(?P<birth_date>\d{2}\.\d{2}\.\d{4})"
)

separator = r"[\s,;]+"

# Enhanced regex to capture full TNM "Tumorstadium" with optional additional info.
# It supports prefixes: c (clinical), p (pathological), and r (recurrent).
regex_tumor = re.compile(
    r"(?P<tumor_status>"
      # T-stage: e.g. cTis, rT4, pT2a, etc.
      r"(?P<T>[cpr]T(?:is|\d+(?:[a-z])?))" + separator +
      # N-stage: e.g. cN0, rNx, pN1a, etc. (allows an optional letter after a digit)
      r"(?P<N>[cpr]N(?:[0-3](?:[a-z])?|x))" + separator +
      # M-stage: e.g. cM0, rM1, pMx (usually just 0, 1, or x)
      r"(?P<M>[cpr]M(?:0|1|x))"
      # Optionally, extra commentary enclosed in parentheses
      r"(?:\s*\([^)]*\))?"
    r")",
    re.IGNORECASE
)

regex_ecog = re.compile(
    r"ECOG:\s*(?P<ecog>[0-5])",
    re.IGNORECASE
)

def extract_patient_data(text):
    """Extract patient data using regex patterns."""
    data = {}
    
    # Extract name and birth date
    name_match = regex_name.search(text)
    if name_match:
        data['name'] = name_match.group("name")
        data['birth_date'] = name_match.group("birth_date")
    
    # Extract tumor status
    tumor_match = regex_tumor.search(text)
    if tumor_match:
        data['tumor_status'] = tumor_match.group("tumor_status")
    
    # Extract ECOG
    ecog_match = regex_ecog.search(text)
    if ecog_match:
        data['ecog'] = ecog_match.group("ecog")
    
    return data

def main():
    # Get all .txt files from processed_output directory
    processed_dir = Path('processed_output')
    all_patients = []
    
    for file_path in processed_dir.glob('*.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            patient_data = extract_patient_data(text)
            if patient_data:
                patient_data['source_file'] = file_path.name
                all_patients.append(patient_data)
    
    # Write results to JSON file
    output_file = 'processed_patients.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_patients, f, ensure_ascii=False, indent=2)
    
    print(f"Processed {len(all_patients)} patients. Results saved to {output_file}")

if __name__ == "__main__":
    main() 