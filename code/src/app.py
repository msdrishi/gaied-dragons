import os
from flask import Flask, render_template, request, jsonify, url_for
from emailExtractEML import extract_eml_content
from emailClassification import classify_email
import json 
app = Flask(__name__)

output_dir = "C:\\Users\\dhaks\\gaied-dragons\\code\\src\\output_attachments" 
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

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        response = classify_email(filepath, output_dir )
        try:
            if isinstance(response, str):  
                response_json = json.loads(response)  
            else:
                response_json = response 
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON response from LLM"}), 500
        
        return jsonify(response_json) 

    return "Invalid file type", 400

if __name__ == "__main__":
    app.run(debug=True)
