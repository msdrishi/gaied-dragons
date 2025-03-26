import os
from RAGTemplate import process_question
from detectDuplicateEmail import process_email
from emailExtractEML import extract_eml_content
from emailExtract import extract_text
from emailEMLPreprocess import clean_text

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

    return response

    # Print the response
    print("User Query:\n", combined_content)
    print("LLM Response:\n", response)
    # Example usage within classify_email function
    status_message = check_duplicate_status(combined_content)
    print("\n\nExisting Issue:", status_message)

# Example usage
if __name__ == "__main__":
    eml_path = "EML_Files\\Sample_EML_Multiple_Mail.eml"  # Replace with the path to your .eml file
    output_dir = "output_attachments"  # Replace with the path to your output directory
    
    classify_email(eml_path, output_dir)