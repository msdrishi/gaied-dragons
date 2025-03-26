from langchain_groq import ChatGroq
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
from langchain_core.documents import Document
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set")

# Load DOCX Documents
doc_path = os.path.abspath("data\\LLM_RAG_Documents\\RequestTypesandSubTypes.docx")
docx_loader = Docx2txtLoader(doc_path)
docs = docx_loader.load()
docx_text = "\n".join([doc.page_content for doc in docs])

# Split Documents into Chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_text(docx_text)

# Convert Chunks to Document Objects for FAISS
chunk_docs = [Document(page_content=chunk) for chunk in chunks]

# Generate Embeddings using HuggingFace
model_name = "sentence-transformers/all-mpnet-base-v2"
embeddings_hf = HuggingFaceEmbeddings(model_name=model_name, model_kwargs={"device": "cpu"})

# Store Embeddings in FAISS Vector Database
vectorstore = FAISS.from_documents(chunk_docs, embeddings_hf)
retriever = vectorstore.as_retriever()

# Configure Groq LLM
os.environ["GROQ_API_KEY"] = groq_api_key
llm = ChatGroq(temperature=0.1, model_name="llama-3.3-70b-versatile")

# Create RAG Chain
rag_template = """Answer the question based only on the following context and retrieve contents in JSON format:
- Request Type
- Sub Request Type
- Reason
- Confidence Level (0-100%)
- Priority (Low, Medium, High)
- Extracted Fields (Personal Information about customer)
- Duplicate Detection (Show "Yes" with an explanation if the issue in the mail content is resolved, or "No" with an explanation if it is not resolved)
- Notes (Any additional information)
{context}
Question: {question}
"""
rag_prompt = ChatPromptTemplate.from_template(rag_template)
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=retriever,
    chain_type_kwargs={"prompt": rag_prompt},
)

# Function to Process Query and Print Output
def process_question(user_question):
    response = qa_chain.invoke(user_question)
    
    # Check if 'result' exists in response, else return full response
    return response.get("result", response)
