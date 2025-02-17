# Medical Report Processing System

This system processes medical reports (specifically discharge letters) to extract and analyze patient data, with a focus on tumor status analysis and patient demographics. It includes functionality for processing Word documents, extracting structured data, and generating comprehensive visualizations.

## Prerequisites

- macOS 10.15 or higher
- Internet connection (for initial setup only)
- Terminal app (comes pre-installed on your Mac)

## Installation for Mac (First Time Setup)

1. Open Terminal:
   - Click the Spotlight search icon (magnifying glass) in the top-right corner of your screen
   - Type "Terminal" and press Enter
   - This will open a command-line interface where you'll type commands

2. Install Homebrew (Mac's package manager):
   - Copy and paste this entire command into Terminal and press Enter:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   - Follow any on-screen instructions (you may need to enter your Mac password)
   - When it asks you to press RETURN to continue, do so

3. Install Python using Homebrew:
   ```bash
   brew install python
   ```
   - This installs Python on your system
   - To verify the installation, type:
   ```bash
   python --version
   ```
   You should see something like "Python 3.x.x"
   
   Note: If `python` command is not found, use `python3` instead. To make `python` work:
   ```bash
   echo 'alias python=python3' >> ~/.zshrc
   source ~/.zshrc
   ```

4. Download this project:
   - Download and install Git (if you haven't already):
   ```bash
   brew install git
   ```
   - Clone (download) this repository:
   ```bash
   cd ~/Documents
   git clone [YOUR_REPOSITORY_URL]
   cd MedParse
   ```
   Replace [YOUR_REPOSITORY_URL] with the actual URL of your repository

5. Set up Python environment:
   ```bash
   # Create a new Python environment (this keeps the project's packages separate from other projects)
   python -m venv venv
   
   # Activate the environment (you'll need to do this each time you work on the project)
   source venv/bin/activate
   
   # Your command prompt should now start with (venv)
   ```

6. Install required packages:
   ```bash
   # Upgrade pip (Python's package installer)
   pip install --upgrade pip
   
   # Install all required packages
   pip install -r requirements.txt
   ```
   This may take a few minutes.

7. Install the German language model:
   ```bash
   python -m spacy download de_core_news_sm
   ```

8. Prepare your data:
   - Create a folder called `Patient_Data` in the project directory if it doesn't exist:
   ```bash
   mkdir -p Patient_Data
   ```
   - Copy your medical report files (*.docx format) into the `Patient_Data` folder
   - You can do this by dragging and dropping files in Finder, or using the command line:
   ```bash
   cp path/to/your/files/*.docx Patient_Data/
   ```

## Using the System

1. Each time you want to use the system:
   - Open Terminal
   - Navigate to the project directory:
   ```bash
   cd ~/Documents/MedParse
   ```
   - Activate the Python environment:
   ```bash
   source venv/bin/activate
   ```
   You'll know it's activated when you see `(venv)` at the start of your Terminal prompt

2. Process your data:
   ```bash
   # Convert documents to text format
   python convert_patient_data_to_txt_mac.py
   
   # Extract patient data
   python extract_patient_data.py
   
   # Analyze tumor status
   python tumor_status_analysis.py
   
   # Check for missing data
   python check_missing_data.py
   ```

3. View visualizations:
   ```bash
   # Start Jupyter Notebook
   jupyter notebook
   ```
   - This will open a new tab in your web browser
   - Click on `VisualizePatients.ipynb`
   - Follow the instructions in the notebook

4. When you're done:
   - Close the Jupyter tab in your browser
   - Return to Terminal and press Ctrl+C to stop Jupyter
   - Type `deactivate` to exit the Python environment

## Troubleshooting for Mac Users

1. If Terminal says "command not found":
   - Make sure you've activated the environment: `source venv/bin/activate`
   - Check if you're in the correct directory: `pwd` should show `/Users/YourUsername/Documents/MedParse`

2. If you see permission errors:
   - Use `sudo` before commands that fail (you'll need to enter your Mac password)
   - Example: `sudo pip install -r requirements.txt`

3. If Python installation fails:
   - Try updating Homebrew: `brew update`
   - Then try again: `brew install python`

4. If you close Terminal and come back later:
   - You'll need to activate the environment again:
   ```bash
   cd ~/Documents/MedParse
   source venv/bin/activate
   ```

5. If you see line ending warnings from Git:
   - This is normal on Mac systems
   - You can ignore these warnings, they won't affect functionality

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
