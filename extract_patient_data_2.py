import re
import json
from pathlib import Path

# --- Define regex patterns ---

# 1. Name and birth date
regex_name = re.compile(
    r"(?P<name>[A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+)+),\s*geb\.\s*am\s*(?P<birth_date>\d{2}\.\d{2}\.\d{4})"
)

separator = r"[\s,;]+"

# 2. Tumor status (TNM) pattern (e.g., cT2b, cNx, cM1)
regex_tumor = re.compile(
    r"(?P<tumor_status>"
      r"(?P<T>[cpr]T(?:is|\d+(?:[a-z])?))" + separator +
      r"(?P<N>[cpr]N(?:[0-3](?:[a-z])?|x))" + separator +
      r"(?P<M>[cpr]M(?:0|1|x))"
      r"(?:\s*\([^)]*\))?"
    r")",
    re.IGNORECASE
)

# 3. ECOG status
regex_ecog = re.compile(
    r"ECOG:\s*(?P<ecog>[0-5])",
    re.IGNORECASE
)

# 4. Vital signs: age, height, weight, BMI
regex_vitals = re.compile(
    r"Alter:\s*(?P<age>\d+).*?Größe:\s*(?P<height>\d+)\s*cm.*?Gewicht:\s*(?P<weight>\d+)\s*kg.*?BMI:\s*(?P<bmi>\d+)",
    re.DOTALL | re.IGNORECASE
)

# 5. Allergies (split by semicolon)
regex_allergies = re.compile(
    r"Allergie:\s*(?P<allergies>.+)",
    re.IGNORECASE
)

# 6. Smoking history: e.g., "Ex-Nikotinabusus bis 11/2024 (ca. 40py)"
regex_smoking = re.compile(
    r"Ex-Nikotinabusus\s+bis\s+(?P<quit_date>\d{1,2}/\d{4}).*?\(ca\.\s*(?P<pack_years>\d+py)\)",
    re.IGNORECASE
)

# 7. PD-L1 information: e.g., "PD-L1 (TPS < 1 %, IC- Score 3 Flächenprozent, CPS 8)"
regex_pdl1 = re.compile(
    r"PD-L1\s*\((?P<pdl1_info>[^)]+)\)",
    re.IGNORECASE
)

# 8. Tumor size (first occurrence in the report)
regex_tumor_size = re.compile(
    r"(?P<size>\d+(?:[.,]\d+)?x\s*\d+(?:[.,]\d+)?x\s*\d+(?:[.,]\d+)?cm)",
    re.IGNORECASE
)

# 9. Diagnoses block: captures text following "Diagnosen:" up to "Verlauf:" or an empty line
regex_diagnoses = re.compile(
    r"Diagnosen:\s*(?P<diagnoses>.+?)(?=\n(?:Verlauf:|$))",
    re.DOTALL | re.IGNORECASE
)

# 10. Medications block: captures text following "Aktuelle Medikation:" until the next marker (e.g., "Mit freundlichen")
regex_medications = re.compile(
    r"Aktuelle Medikation:\s*(?P<medications>.*?)\n(?:Mit freundlichen|$)",
    re.DOTALL | re.IGNORECASE
)

# --- Extraction function ---

def extract_patient_data(text):
    """Extract patient data using regex patterns."""
    data = {}
    
    # Extract name and birth date
    name_match = regex_name.search(text)
    if name_match:
        data['name'] = name_match.group("name")
        data['birth_date'] = name_match.group("birth_date")
    
    # Extract tumor status (TNM)
    tumor_match = regex_tumor.search(text)
    if tumor_match:
        data['tumor_status'] = tumor_match.group("tumor_status")
    
    # Extract ECOG status
    ecog_match = regex_ecog.search(text)
    if ecog_match:
        data['ecog'] = ecog_match.group("ecog")
    
    # Extract vital signs: age, height, weight, BMI
    vitals_match = regex_vitals.search(text)
    if vitals_match:
        data['age'] = vitals_match.group("age")
        data['height'] = vitals_match.group("height")
        data['weight'] = vitals_match.group("weight")
        data['bmi'] = vitals_match.group("bmi")
    
    # Extract allergies (split by semicolon)
    allergies_match = regex_allergies.search(text)
    if allergies_match:
        allergies = allergies_match.group("allergies")
        data['allergies'] = [a.strip() for a in allergies.split(';')]
    
    # Extract smoking history (quit date and pack years)
    smoking_match = regex_smoking.search(text)
    if smoking_match:
        data['quit_date'] = smoking_match.group("quit_date")
        data['pack_years'] = smoking_match.group("pack_years")
    
    # Extract PD-L1 information
    pdl1_match = regex_pdl1.search(text)
    if pdl1_match:
        data['pd_l1'] = pdl1_match.group("pdl1_info").strip()
    
    # Extract tumor size (first occurrence)
    tumor_size_match = regex_tumor_size.search(text)
    if tumor_size_match:
        data['tumor_size'] = tumor_size_match.group("size")
    
    # Extract diagnoses block
    diagnoses_match = regex_diagnoses.search(text)
    if diagnoses_match:
        data['diagnoses'] = diagnoses_match.group("diagnoses").strip()
    
    # Extract medications block
    medications_match = regex_medications.search(text)
    if medications_match:
        data['medications'] = medications_match.group("medications").strip()
    
    return data

# --- Main routine to process files ---

def main():
    # Get all .txt files from the processed_output directory
    processed_dir = Path('processed_output')
    all_patients = []
    
    for file_path in processed_dir.glob('*.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            patient_data = extract_patient_data(text)
            if patient_data:
                patient_data['source_file'] = file_path.name
                all_patients.append(patient_data)
    
    # Write results to a JSON file
    output_file = 'processed_patients.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_patients, f, ensure_ascii=False, indent=2)
    
    print(f"Processed {len(all_patients)} patients. Results saved to {output_file}")

if __name__ == "__main__":
    main()
