import faiss
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 📌 File paths for persistent storage
DB_PATH = "faiss_index.bin"
EMAILS_PATH = "emails.pkl"

# 📌 Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# 📌 Initialize FAISS index
embedding_dim = 384  
index = faiss.IndexFlatL2(embedding_dim)  
email_store = []  # Store email texts

# 📌 Generate sentence embeddings
def get_embedding(text):
    return model.encode(text).astype('float32')

# 📌 Check for duplicate emails
def is_duplicate_email(email_body, threshold=0.8):
    new_embedding = get_embedding(email_body).reshape(1, -1)

    if index.ntotal > 0:
        stored_embeddings = np.array([get_embedding(e) for e in email_store])
        similarities = cosine_similarity(new_embedding, stored_embeddings)[0]
        
        max_similarity = np.max(similarities)
        best_match_idx = np.argmax(similarities)


        if max_similarity >= threshold:
            return True, email_store[best_match_idx]

    return False, None

# 📌 Process an email
def process_email(email_body):
    duplicate, matched_email = is_duplicate_email(email_body)

    if duplicate:
        return 'duplicate'


    # Store new email
    new_embedding = get_embedding(email_body)
    index.add(new_embedding.reshape(1, -1))  
    email_store.append(email_body)
    save_data()

# 📌 Save FAISS index, emails
def save_data():
    faiss.write_index(index, DB_PATH)
    with open(EMAILS_PATH, "wb") as f:
        pickle.dump(email_store, f)

# 📌 Load FAISS index, emails
def load_data():
    global index, email_store, llm_results
    if os.path.exists(DB_PATH):
        index = faiss.read_index(DB_PATH)
    if os.path.exists(EMAILS_PATH):
        with open(EMAILS_PATH, "rb") as f:
            email_store = pickle.load(f)

