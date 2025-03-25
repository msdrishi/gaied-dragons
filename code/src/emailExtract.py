import PyPDF2
from docx import Document
import win32com.client
import pytesseract
from PIL import Image
import re

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_text_from_doc(doc_path):
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc = word.Documents.Open(doc_path)
    text = doc.Content.Text
    doc.Close(False)
    word.Quit()
    return text

def extract_text_from_jpg(jpg_path):
    text = pytesseract.image_to_string(Image.open(jpg_path))
    return text

def preprocess_text(text):
    # Convert text to lowercase
    # text = text.lower()
    # Remove email addresses
    # text = re.sub(r'\S+@\S+', '', text)
    # Remove URLs
    # text = re.sub(r'http\S+|www\S+', '', text)
    # Remove special characters and numbers
    # text = re.sub(r'[^a-z\s]', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_text(file_path):
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
    # Print the extracted text before preprocessing
    # print("Extracted Text Before Preprocessing:")
    # print(text)
    # Preprocess the extracted text
    # print("Extracted Text After Preprocessing:")
    text = preprocess_text(text)  
    return text
