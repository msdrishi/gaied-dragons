import PyPDF2
from docx import Document
import win32com.client
import pytesseract
from PIL import Image
import re

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def extract_text_from_pdf(file_path):
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except PyPDF2.errors.PdfReadError:
        print(f"Error: Unable to read the PDF file at {file_path}. It may be corrupted or invalid.")
        return ""  # Return an empty string if the PDF is invalid
    except Exception as e:
        print(f"Unexpected error while processing the PDF file at {file_path}: {e}")
        return ""  # Return an empty string for any other exceptions

def extract_text_from_docx(docx_path):
    try:
        doc = Document(docx_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        print(f"Error while processing the DOCX file at {docx_path}: {e}")
        return ""  # Return an empty string for any exceptions

def extract_text_from_doc(doc_path):
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc = word.Documents.Open(doc_path)
        text = doc.Content.Text
        doc.Close(False)
        word.Quit()
        return text
    except Exception as e:
        print(f"Error while processing the DOC file at {doc_path}: {e}")
        return ""  # Return an empty string for any exceptions

def extract_text_from_jpg(jpg_path):
    try:
        text = pytesseract.image_to_string(Image.open(jpg_path))
        return text
    except Exception as e:
        print(f"Error while processing the JPG file at {jpg_path}: {e}")
        return ""  # Return an empty string for any exceptions

def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_text(file_path):
    try:
        if file_path.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            text = extract_text_from_docx(file_path)
        elif file_path.endswith('.doc'):
            text = extract_text_from_doc(file_path)
        elif file_path.endswith('.jpg'):
            text = extract_text_from_jpg(file_path)
        else:
            raise ValueError("Unsupported file format")
        text = preprocess_text(text)  
        return text
    except Exception as e:
        print(f"Error while extracting text from file {file_path}: {e}")
        return ""  # Return an empty string for any exceptions