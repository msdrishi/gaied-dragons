import os
import re
from modules.retrieval.RAGTemplate import process_question
from modules.classification.detectDuplicateEmail import process_email
from modules.preprocessing.emailExtractEML import extract_eml_content
from modules.preprocessing.emailExtract import extract_text
from modules.preprocessing.emailEMLPreprocess import clean_text

def check_duplicate_status(combined_content):
        if process_email(combined_content) == 'duplicate':
            return "This issue has already been reported by the other customer."
        else:
            return "This is a new issue reported by the customer."


def classify_email(eml_path, output_dir):
    # Extract content from .eml file
    eml_content = extract_eml_content(eml_path, output_dir)
    # Preprocess the extracted email content
    preprocessed_content = clean_text(eml_content)
    # Check for attachments and process them
    attachments_info = ""
    for filename in os.listdir(output_dir):
        if filename.endswith(('.pdf', '.docx', '.doc', '.jpg')):
            file_path = os.path.join(output_dir, filename)
            attachment_text = extract_text(file_path)
            attachment_text = clean_text(attachment_text)
            attachments_info += f"\n({filename}):\n{attachment_text}\n"
    # Remove all files in the output directory after processing attachments
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    # Combine email content and attachments info
    if attachments_info:
        attachments_info = '\n\nAttachments Details\n' + attachments_info

    combined_content = preprocessed_content + attachments_info
    
    # Call the LLM for classification
    response = process_question(combined_content)
    clean_response = re.sub(r"```json|```", "", response).strip()
    clean_response = clean_response[:-1]
    status = ',\n  "Existing Issue": "' + check_duplicate_status(combined_content) + '"\n}'
    clean_response = clean_response + status
    return clean_response
