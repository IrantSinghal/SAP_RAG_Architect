import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
DB_DIR = os.path.join(BASE_DIR, "sap_db")

def initialize_knowledge_base():
    os.makedirs(DOCS_DIR, exist_ok=True)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Try loading existing DB
    if os.path.exists(DB_DIR) and os.listdir(DB_DIR):
        return Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

    # Otherwise process docs
    if not os.path.exists(DOCS_DIR):
        return None
        
    loader = PyPDFDirectoryLoader(DOCS_DIR)
    documents = loader.load()
    if not documents:
        return None
        
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=250, separators=["\n\n", "\n", " ", ""])
    chunks = text_splitter.split_documents(documents)
    return Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=DB_DIR)
