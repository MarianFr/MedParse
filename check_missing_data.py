import json
import pandas as pd
from collections import defaultdict

def analyze_missing_data(json_file):
    # Read the JSON file
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Initialize dictionaries to store missing data information
    missing_counts = defaultdict(int)
    missing_sources = defaultdict(list)
    
    # Expected fields
    expected_fields = ['name', 'birth_date', 'gender', 'tumor_status', 'ecog', 'source_file']
    
    # Check each record for missing data
    for idx, record in df.iterrows():
        for field in expected_fields:
            if field not in record or pd.isna(record[field]) or record[field] == "":
                missing_counts[field] += 1
                missing_sources[field].append(record['source_file'])
    
    # Print summary statistics
    print("\n=== Missing Data Analysis ===\n")
    print("Total number of records:", len(df))
    print("\nMissing data counts:")
    print("-" * 40)
    
    for field in expected_fields:
        if missing_counts[field] > 0:
            print(f"\n{field}:")
            print(f"  Missing in {missing_counts[field]} records ({(missing_counts[field]/len(df)*100):.1f}%)")
            print("  Missing in files:")
            for source in sorted(set(missing_sources[field])):
                print(f"    - {source}")
    
    # Additional Analysis
    print("\n=== Data Quality Analysis ===\n")
    
    # Analyze tumor_status components
    if 'tumor_status' in df.columns:
        tumor_status_missing_components = defaultdict(list)
        for idx, record in df.iterrows():
            if pd.notna(record['tumor_status']):
                status = record['tumor_status']
                if 'T' not in status:
                    tumor_status_missing_components['T'].append(record['source_file'])
                if 'N' not in status:
                    tumor_status_missing_components['N'].append(record['source_file'])
                if 'M' not in status:
                    tumor_status_missing_components['M'].append(record['source_file'])
        
        print("Tumor Status Component Analysis:")
        print("-" * 40)
        for component in ['T', 'N', 'M']:
            if tumor_status_missing_components[component]:
                print(f"\nMissing {component} component in tumor_status:")
                for source in sorted(set(tumor_status_missing_components[component])):
                    print(f"  - {source}")
    
    # Check for potentially invalid values
    print("\nPotential Data Issues:")
    print("-" * 40)
    
    # Check ECOG values
    if 'ecog' in df.columns:
        invalid_ecog = df[~df['ecog'].astype(str).str.match(r'^[0-4]$|^[0-4]-[0-4]$|^$|^nan$', na=True)]
        if not invalid_ecog.empty:
            print("\nUnusual ECOG values:")
            for _, record in invalid_ecog.iterrows():
                print(f"  - {record['source_file']}: ECOG = {record['ecog']}")
    
    # Check gender values
    if 'gender' in df.columns:
        invalid_gender = df[~df['gender'].str.lower().isin(['male', 'female', ''])]
        if not invalid_gender.empty:
            print("\nUnusual gender values:")
            for _, record in invalid_gender.iterrows():
                print(f"  - {record['source_file']}: gender = {record['gender']}")

if __name__ == "__main__":
    analyze_missing_data('processed_patients.json') 