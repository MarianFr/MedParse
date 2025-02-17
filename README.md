# Medical Report Processing System

This system processes medical reports (specifically discharge letters) to extract and visualize patient data. It includes functionality for processing Word documents, extracting structured data, and presenting it through a web interface.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation for Mac Users (First Time Setup)

1. Install Python:
   - Open Terminal (press Cmd + Space, type "Terminal" and press Enter)
   - Install Homebrew (Mac's package manager) if you don't have it:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   - Install Python using Homebrew:
   ```bash
   brew install python
   ```
   - Verify the installation:
   ```bash
   python3 --version
   ```
   You should see Python 3.x.x printed in the terminal.

   - (Optional) To use `python` instead of `python3`, add these lines to your shell profile (~/.zshrc or ~/.bash_profile):
   ```bash
   alias python=python3
   alias pip=pip3
   ```
   Then reload your profile:
   ```bash
   source ~/.zshrc  # if using zsh
   # OR
   source ~/.bash_profile  # if using bash
   ```
   After this, you can use `python` and `pip` commands instead of `python3` and `pip3`.

2. Clone this repository or download the source code.

3. Open Terminal and navigate to the project directory:
   ```bash
   cd path/to/your/project
   ```
   (Replace "path/to/your/project" with the actual path where you saved the project)

4. Create and activate a virtual environment:
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate
   ```
   When the virtual environment is activated, you'll see `(venv)` at the beginning of your terminal prompt.

5. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

6. Add your medical report files:
   - Place your medical report files (*.docx format) in the `Patient_Data/` directory
   - The system expects Word documents (.docx files) containing medical discharge letters
   - Make sure the documents follow the expected format for proper data extraction

## Project Structure

- `Patient_Data/` - Directory containing input Word documents (add your .docx files here)
- `processed_output/` - Directory containing processed text files (automatically generated)
- `templates/` - HTML templates for the web interface
- `app.py` - Flask web application
- `extract_patient_data.py` - Script for processing medical reports
- `extract_patient_data_2.py` - Enhanced version of the processing script

## Usage

1. Make sure your virtual environment is activated. If you just followed the installation steps, it should be. If not, activate it:
   ```bash
   source venv/bin/activate
   ```
   You'll know it's activated when you see `(venv)` at the start of your terminal prompt.

2. Place your medical reports (Word documents) in the `Patient_Data/` directory.

3. Process the documents by running:
   ```bash
   python extract_patient_data_2.py
   ```
   This will create processed text files in the `processed_output/` directory and generate a JSON file with structured patient data.

4. Start the web application:
   ```bash
   python app.py
   ```

5. Open your web browser and navigate to `http://127.0.0.1:5000` to view the dashboard.

6. When you're done, you can deactivate the virtual environment by typing:
   ```bash
   deactivate
   ```

Note: If you close your Terminal and come back later, you'll need to:
1. Navigate back to your project directory (`cd path/to/your/project`)
2. Reactivate the virtual environment (`source venv/bin/activate`)
3. Then you can run the scripts again
