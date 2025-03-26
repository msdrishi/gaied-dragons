import re

def clean_text(input_text):
    if not input_text:
        return input_text
    
    # Extract and format the header
    header_pattern = re.search(r'subject: (.*)\nfrom: (.*) <(.*)>\nto: (.*) <(.*)>\ndate: (.*)', input_text, re.IGNORECASE)
    
    if header_pattern:
        subject = header_pattern.group(1).strip()
        from_email = header_pattern.group(3).strip()
        to_email = header_pattern.group(5).strip()
        date = header_pattern.group(6).strip()
        
        formatted_header = f"Date : {date}\nSubject: {subject} from {from_email} to {to_email}\n"
    else:
        formatted_header = ""
    
    # Remove the header from the input text
    input_text = re.sub(r'subject: .*?\nfrom: .*?\nto: .*?\ndate: .*?\nbody:', '', input_text, flags=re.IGNORECASE | re.DOTALL)
    
    # Format inline date and email from 'On Sat, ... wrote:' lines
    input_text = re.sub(r'On (.*) at .*? ([^ ]+@[^ ]+) wrote:', lambda m: f"Date {m.group(1)} from {m.group(2).replace('@', '').replace('.', '')}", input_text)
    
    # Remove all special characters except spaces using regex for the rest of the content
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', input_text)
    
    # Replace multiple spaces with a single space and strip leading/trailing spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # Ensure date and email are on the same line
    cleaned = re.sub(r'(Date .*? from [^ ]+)', r'\1', cleaned)
    
    # Add line breaks between different sections
    cleaned = re.sub(r'(Date .*? from [^ ]+)', r'\n\n\1\n\n', cleaned)
    
    # Remove the "Thanks/Regards" section at the end of the email content
    cleaned = re.sub(r'(Thank you for your prompt support|Sincerely|Regards|Thanks).*', '', cleaned, flags=re.IGNORECASE).strip()
    
    return formatted_header + '\n' + cleaned
