import spacy
import re
import json
from pathlib import Path

def extract_patient_info(text):
    info = {}
    # Load the German spaCy model - ensure the model is installed.
    try:
        nlp = spacy.load("de_core_news_sm")
    except OSError as e:
        print("Error: Model 'de_core_news_sm' not found. Please run: python -m spacy download de_core_news_sm")
        raise e
    doc = nlp(text)

    # --- Extract Tumorstatus ---
    # First try to capture the tumor status from explicit markers ("Tumorstadium:" or "Stadium:")
    # The regex stops capturing when it encounters an optional ", UICC:" (or end-of-line)
    tumor_match = re.search(
        r"(?:Tumorstadium:|Stadium:)\s*(?:TNM:\s*)?(.+?)(?=,?\s*UICC:|\n|$)",
        text,
        re.IGNORECASE
    )
    if tumor_match:
        info["tumor_status"] = tumor_match.group(1).strip()
    else:
        # Fallback: Suche nach einem typischen TNM-Muster,
        # z.B. "cT2b, cNx, cM1" (inklusiv möglicher Zusätze am Ende).
        tnm_fallback = re.search(
            r"([cpr]T(?:is|\d+[a-z]?))[\s,;]+([cpr]N(?:[0-3][a-z]?|x))[\s,;]+([cpr]M(?:0|1|x))",
            text,
            re.IGNORECASE
        )
        if tnm_fallback:
            info["tumor_status"] = tnm_fallback.group(0).strip()

    # --- Extract ECOG Status ---
    # Look for ECOG values in various formats:
    # (ECOG 2-3), ECOG: 1, (ECOG2), (ECOG4), etc.
    ecog_match = re.search(
        r"""
        # Match various ECOG patterns (with or without parentheses)
        (?:
            \(?                  # Optional opening parenthesis
            ECOG[\s:-]*         # ECOG followed by optional space, colon, or hyphen
            (?:                 # Value group
                (\d)            # First digit
                (?:             # Optional range group
                    \s*-\s*     # Hyphen with optional spaces
                    (\d)        # Second digit
                )?              # Range is optional
            )
            \)?                 # Optional closing parenthesis
        )
        """,
        text,
        re.VERBOSE | re.IGNORECASE  # Allow for verbose regex and case insensitivity
    )
    if ecog_match:
        # Extract both numbers if it's a range
        first_value = ecog_match.group(1)
        second_value = ecog_match.group(2) if ecog_match.group(2) else None
        
        if second_value:
            info["ecog"] = f"{first_value}-{second_value}"
        else:
            info["ecog"] = first_value

    # --- Extract Birth Date ---
    # Search for a birthdate pattern like "geb. am 15.06.1955" (case-insensitive)
    birth_date_match = re.search(r"geb\.\s*am\s*(\d{2}\.\d{2}\.\d{4})", text, re.IGNORECASE)
    if birth_date_match:
        info["birth_date"] = birth_date_match.group(1).strip()

    # --- Extract Patient Name & Gender using NER ---
    # We attempt to find the sentence that contains the patient details.
    patient_name = None
    target_sentence = None
    for sent in doc.sents:
        if "wir berichten über" in sent.text:
            target_sentence = sent.text
            break

    # Fallback: if no sentence with "wir berichten über" is found,
    # search the entire text for a pattern that includes a name and a birth date.
    if not target_sentence:
        fallback_pattern = r"(Herrn|Frau)\s+[A-ZÄÖÜ][a-zäöüß]+,\s*[A-ZÄÖÜ][a-zäöüß]+,\s*geb\.\s*am\s*\d{1,2}\.\d{1,2}\.\d{4}"
        fallback_match = re.search(fallback_pattern, text, re.IGNORECASE)
        if fallback_match:
            target_sentence = fallback_match.group(0)

    if target_sentence:
        # Try pattern 1: expecting "Herrn|Frau <Firstname> <Lastname>,"
        name_match = re.search(
            r"(Herrn|Frau)\s+([A-ZÄÖÜ][a-zäöüß]+)\s+([A-ZÄÖÜ][a-zäöüß]+),",
            target_sentence
        )
        if name_match:
            title = name_match.group(1)
            first_name = name_match.group(2)
            last_name = name_match.group(3)
            patient_name = f"{first_name} {last_name}"
        else:
            # Fallback pattern: "Herrn|Frau <Lastname>, <Firstname>"
            name_match = re.search(
                r"(Herrn|Frau)\s+([A-ZÄÖÜ][a-zäöüß]+),\s*([A-ZÄÖÜ][a-zäöüß]+)",
                target_sentence
            )
            if name_match:
                title = name_match.group(1)
                last_name = name_match.group(2)
                first_name = name_match.group(3)
                patient_name = f"{first_name} {last_name}"
            else:
                # Fallback using spaCy's PERSON entities
                sent_doc = nlp(target_sentence)
                people = [ent.text for ent in sent_doc.ents if ent.label_ == "PER"]
                if people:
                    patient_name = people[0]

    if patient_name:
        info["name"] = patient_name
    else:
        # Fallback: Suche im gesamten Text nach einem Muster, 
        # das einen Namen und ein Geburtsdatum enthält.
        fallback_names = re.findall(
            r"(Herrn|Frau)\s+([A-ZÄÖÜ][a-zäöüß]+),\s*([A-ZÄÖÜ][a-zäöüß]+)\s*,?\s*geb\.\s*am\s*\d{1,2}\.\d{1,2}\.\d{4}",
            text,
            re.IGNORECASE
        )
        if fallback_names:
            fallback_match = fallback_names[-1]
            fallback_title = fallback_match[0]  # Wird für die Geschlechtsbestimmung verwendet
            last_name = fallback_match[1]
            first_name = fallback_match[2]
            patient_name = f"{first_name} {last_name}"
            info["name"] = patient_name
        else:
            info["name"] = None

    # Bestimme das Geschlecht anhand des extrahierten Titels (wenn vorhanden),
    # ansonsten anhand der target_sentence.
    if 'fallback_title' in locals() and fallback_title:
        if re.search(r"\bFrau\b", fallback_title, re.IGNORECASE):
            info["gender"] = "female"
        elif re.search(r"\bHerrn?\b", fallback_title, re.IGNORECASE):
            info["gender"] = "male"
        else:
            info["gender"] = "unknown"
    elif target_sentence:
        if re.search(r"\bFrau\b", target_sentence, re.IGNORECASE):
            info["gender"] = "female"
        elif re.search(r"\bHerrn?\b", target_sentence, re.IGNORECASE):
            info["gender"] = "male"
        else:
            info["gender"] = "unknown"
    else:
        info["gender"] = "unknown"

    return info

def main():
    processed_dir = Path("processed_output")
    all_patients = []

    for file_path in processed_dir.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            patient_info = extract_patient_info(text)
            if patient_info:
                patient_info["source_file"] = file_path.name
                all_patients.append(patient_info)

    output_file = "processed_patients.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_patients, f, ensure_ascii=False, indent=2)

    print(f"Processed {len(all_patients)} patients. Results saved to {output_file}")

if __name__ == "__main__":
    main() 