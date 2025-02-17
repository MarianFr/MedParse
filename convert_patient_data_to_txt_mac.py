from docx import Document
import pdfplumber
import nltk
from nltk.tokenize import word_tokenize
import os
import time
import subprocess
import shutil
from tqdm import tqdm

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
except Exception as e:
    print(f"Warning: Could not download NLTK data: {str(e)}")

def convert_to_pdf(input_path, pdf_path):
    original_dir = os.getcwd()
    try:
        # Try to locate the LibreOffice executable
        soffice_path = shutil.which("soffice")
        if soffice_path is None:
            soffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"
            if not os.path.exists(soffice_path):
                raise FileNotFoundError("LibreOffice not found. Please install LibreOffice.")
        
        # Get absolute paths and ensure they use backslashes
        abs_input_path = os.path.abspath(input_path).replace('/', '\\')
        abs_pdf_path = os.path.abspath(pdf_path).replace('/', '\\')
        abs_output_dir = os.path.dirname(abs_pdf_path)
        
        # Create output directory if it doesn't exist
        if not os.path.exists(abs_output_dir):
            os.makedirs(abs_output_dir)
        
        # Run LibreOffice conversion directly in the output directory
        os.chdir(abs_output_dir)
        
        # Run LibreOffice conversion
        cmd = [
            soffice_path,
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', abs_output_dir,
            abs_input_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return False
        
        # Give LibreOffice some time to finish writing the file
        time.sleep(2)
        
        # Get the expected output filename
        expected_name = os.path.splitext(os.path.basename(input_path))[0] + '.pdf'
        expected_path = os.path.join(abs_output_dir, expected_name)
        
        # Verify and move the PDF if needed
        if os.path.exists(expected_path):
            if expected_path.lower() != abs_pdf_path.lower():
                if os.path.exists(abs_pdf_path):
                    os.remove(abs_pdf_path)
                shutil.move(expected_path, abs_pdf_path)
            return True
        return False
        
    except Exception:
        return False
        
    finally:
        try:
            os.chdir(original_dir)
        except:
            pass

def extract_text_from_pdf(pdf_path):
    full_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                lines = page_text.split('\n')
                if len(lines) > 6:
                    header = '\n'.join(lines[:3])
                    main_content = '\n'.join(lines[3:-3])
                    footer = '\n'.join(lines[-3:])
                    full_text.append(f"\n=== Page {i} ===")
                    full_text.append(f"--- Header ---\n{header}")
                    full_text.append(f"--- Content ---\n{main_content}")
                    full_text.append(f"--- Footer ---\n{footer}")
                else:
                    full_text.append(f"\n=== Page {i} ===")
                    full_text.append(page_text)
    return '\n'.join(full_text)

def process_docx(input_path, output_path):
    try:
        # Ensure we use absolute paths
        abs_output_path = os.path.abspath(output_path)
        abs_input_path = os.path.abspath(input_path)
        pdf_path = os.path.join(os.path.dirname(abs_output_path), 
                               os.path.splitext(os.path.basename(abs_input_path))[0] + '.pdf')
        
        # Convert DOCX to PDF using LibreOffice
        if not convert_to_pdf(abs_input_path, pdf_path):
            raise Exception("PDF conversion failed")
        
        text = extract_text_from_pdf(pdf_path)
        
        with open(abs_output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        tokens = word_tokenize(text)
        
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        
        return len(tokens)
        
    except Exception as e:
        print(f"Error processing {os.path.basename(input_path)}: {str(e)}")
        return None

if __name__ == "__main__":
    # Create output directory if it doesn't exist
    output_dir = "processed_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        input_dir = "patient_data"
        if not os.path.exists(input_dir):
            print(f"Error: Input directory '{input_dir}' does not exist!")
            exit(1)

        # Exclude temporary files starting with ~$
        docx_files = [f for f in os.listdir(input_dir)
                      if f.endswith('.docx') and not f.startswith('~$')]
        
        if not docx_files:
            print(f"No .docx files found in {input_dir}")
            exit(1)

        print(f"Processing {len(docx_files)} files...")
        
        total_tokens = 0
        processed_files = 0
        
        # Process files with progress bar
        for docx_file in tqdm(docx_files, desc="Converting documents", unit="file"):
            input_path = os.path.join(input_dir, docx_file)
            base_name = os.path.splitext(docx_file)[0]
            output_path = os.path.join(output_dir, f"{base_name}.txt")
            
            tokens = process_docx(input_path, output_path)
            if tokens:
                total_tokens += tokens
                processed_files += 1
        
        # Print summary
        print(f"\nProcessed {processed_files}/{len(docx_files)} files successfully")
        if processed_files > 0:
            print(f"Total tokens extracted: {total_tokens}")
            print(f"Average tokens per file: {total_tokens // processed_files}")
            
    except KeyboardInterrupt:
        print("\nProcessing interrupted by user")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    finally:
        pass
