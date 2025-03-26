import os
from flask import Flask, render_template, request, jsonify, url_for
from modules.classification.emailClassification import classify_email  # Update this
from modules.preprocessing.emailExtractEML import extract_eml_content  # Upd
import json 
import re

app = Flask(__name__)

output_dir = "src\\output_attachments" 
# Configure upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = {"pdf", "eml", "txt", "docx"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.route("/")
def index():
    return render_template("upload.html")


def clean_json_response(response):
    """Clean the JSON response by removing unwanted formatting."""
    # Remove triple backticks and language hints (```json, ```).
    clean_response = re.sub(r"```json|```", "", response).strip()
    
    try:
        return json.loads(clean_response)  # Convert to a valid JSON object
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response from LLM", "raw_response": response}

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        
        response = classify_email(filepath, output_dir)  

        # Remove all files in the output directory after processing attachments
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        clean_response = clean_json_response(response)
        if not isinstance(clean_response, dict):
            return jsonify({"error": "Invalid response format"}), 500  

        return jsonify(clean_response)  

    return jsonify({"error": "Invalid file type"}), 400

if __name__ == "__main__":
    app.run(debug=True)
