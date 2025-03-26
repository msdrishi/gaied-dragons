# 🚀 Project Name

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction

This project automates the routing and classification of incoming customer emails in the commercial banking sector using GenAI. It extracts email content, classifies request types, detects duplicates, and reduces manual effort for faster response times.

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](link-to-image)

## 💡 Inspiration
Processing high volumes of customer emails manually is time-consuming and prone to errors. This solution uses GenAI to streamline email management by classifying requests, detecting duplicates, and extracting key information.

## ⚙️ What It Does
Email Extraction: Extracts email content from .eml files and attachments (.pdf, .docx, .doc, .jpg).

Classification: Uses GenAI to classify emails into predefined request types and sub-types.

Duplicate Detection: Leverages FAISS for vector similarity search to identify duplicate emails.

## 🛠️ How We Built It
GenAI Model: LLM using Groqcloud with LLaMA 3.3 70B for accurate classification.

Duplicate Detection: FAISS for efficient vector-based similarity search.

Data Extraction: PyPDF2, docx, win32com, and Tesseract OCR for content extraction.

Embedding Generation: HuggingFace models to generate embeddings.

Document Management: DOCX files containing request types and sub-types.

Vector Storage: FAISS Vector Database for similarity comparisons.

Backend: Python (Flask/FastAPI).

Additional Libraries: Sentence Transformers, NumPy, and Scikit-Learn

## 🚧 Challenges We Faced
Fine-tuning the LLM to improve classification accuracy.

Managing large-scale email data efficiently.

Ensuring low false positives in duplicate detection.

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/your-repo.git
   ```
2. Install dependencies  
   ```sh
   npm install  # or pip install -r requirements.txt (for Python)
   ```
3. Run the project  
   ```sh
   npm start  # or python app.py
   ```

## 🏗️ Tech Stack
- 🔹 Frontend: React / Vue / Angular
- 🔹 Backend: Node.js / FastAPI / Django
- 🔹 Database: PostgreSQL / Firebase
- 🔹 Other: OpenAI API / Twilio / Stripe

## 👥 Team
- **Your Name** - [GitHub](#) | [LinkedIn](#)
- **Teammate 2** - [GitHub](#) | [LinkedIn](#)
