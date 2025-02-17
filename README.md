# Medical Report Processing System

This system processes medical reports (specifically discharge letters) to extract and analyze patient data, with a focus on tumor status analysis and patient demographics. It includes functionality for processing Word documents, extracting structured data, and generating comprehensive visualizations.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation

1. Clone this repository or download the source code.

2. Create and activate a virtual environment:
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment (Windows)
   venv\Scripts\activate
   
   # Activate virtual environment (Mac/Linux)
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Download the required spaCy model:
   ```bash
   python -m spacy download de_core_news_sm
   ```

5. Add your medical report files:
   - Place your medical report files (*.docx format) in the `Patient_Data/` directory
   - The system expects Word documents (.docx files) containing medical discharge letters

## Project Structure

- `Patient_Data/` - Directory for input Word documents
- `processed_output/` - Directory containing processed text files
- `extract_patient_data.py` - Main script for processing medical reports
- `convert_patient_data_to_txt_windows.py` - Windows-specific conversion script
- `convert_patient_data_to_txt_mac.py` - Mac-specific conversion script
- `tumor_status_analysis.py` - Script for analyzing tumor status data
- `check_missing_data.py` - Script for identifying missing or incomplete data
- `VisualizePatients.ipynb` - Jupyter notebook for data visualization
- `processed_patients.json` - Structured output of processed patient data

## Features

### 1. Data Extraction
- Processes medical discharge letters in Word format
- Extracts key patient information including:
  - Demographic data
  - Tumor status (TNM classification)
  - ECOG scores
  - Treatment information

### 2. Data Analysis
- Tumor status analysis with detailed TNM classification
- Patient demographics visualization
- Statistical analysis of medical parameters
- Missing data identification and reporting

### 3. Visualization
The system provides comprehensive visualization capabilities through both Python scripts and Jupyter notebooks:

#### Tumor Status Analysis (`tumor_status_analysis.py`)
- Complete tumor status distribution
- Individual T, N, M stage distributions
- Stage correlation heatmaps
- Stage prefix analysis (c/p)
- Network visualization of stage combinations

#### Patient Visualization (`VisualizePatients.ipynb`)
- Gender distribution
- Age demographics
- ECOG score analysis
- Interactive plots and charts

## Usage

1. Data Processing:
   ```bash
   # For Windows users
   python convert_patient_data_to_txt_windows.py
   
   # For Mac users
   python convert_patient_data_to_txt_mac.py
   ```

2. Extract Patient Data:
   ```bash
   python extract_patient_data.py
   ```

3. Analyze Tumor Status:
   ```bash
   python tumor_status_analysis.py
   ```

4. Check for Missing Data:
   ```bash
   python check_missing_data.py
   ```

5. For detailed visualizations, open and run `VisualizePatients.ipynb` in Jupyter:
   ```bash
   jupyter notebook VisualizePatients.ipynb
   ```

## Output

- Processed text files in `processed_output/`
- Structured JSON data in `processed_patients.json`
- Visualization plots in respective directories
- Analysis reports and statistics

## Notes

- The system is designed to handle German medical reports
- Ensure proper encoding (UTF-8) for all input files
- Regular expressions and NLP models are optimized for German medical terminology
- The visualization tools are designed to handle missing or incomplete data gracefully

## Troubleshooting

1. If you encounter encoding issues:
   - Ensure all input files are in UTF-8 format
   - Use the appropriate conversion script for your operating system

2. If spaCy model fails to load:
   - Ensure you've run `python -m spacy download de_core_news_sm`
   - Check your Python environment is activated

3. For visualization issues:
   - Ensure all required dependencies are installed
   - Check Jupyter notebook kernel is using the correct environment
