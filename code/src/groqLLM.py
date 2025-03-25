from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json
from flask import Flask, request, jsonify

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "llama-3.3-70b-versatile"  # The model you want to use

# Initialize ChatGroq
llm = ChatGroq(api_key=API_KEY, model_name=MODEL_NAME)

def classify_query(query):
    response = llm.invoke(f"""
You are a banking AI assistant. Respond **ONLY with JSON**, without explanations.

Return JSON like this:
{{
    "request_type": "Loan Modification",
    "sub_request_type": "Interest Rate Adjustment",
    "reason": "Current market conditions may allow for a lower interest rate",
    "confidence": 90,
    "priority": "Medium"
}}

User Query: {query}
""")

    print("Raw LLM Response:", response)  # Debugging

    # Ensure response is a string before parsing
    if hasattr(response, "content"):  
        response_text = response.content.strip()
    elif isinstance(response, str):  
        response_text = response.strip()
    else:
        return json.dumps({"error": "Invalid response from AI model"})

    try:
        # Convert string response to a valid JSON dictionary
        json_response = json.loads(response_text)

        # Ensure the function returns a JSON serializable dictionary
        return json_response  
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response from LLM1"}

# Example usage
if __name__ == "__main__":
    query = " I am facing issues with my online banking account. I can't log in and I need help to reset my password"
    result = classify_query(query)
    print("LLM Response:", result)