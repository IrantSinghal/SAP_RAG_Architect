import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

# Define the path to your database folder
DB_DIR = os.path.join(os.getcwd(), "sap_db")

def initialize_knowledge_base():
    # FastEmbed is optimized for CPU/Serverless environments
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    # Load the existing database
    if os.path.exists(DB_DIR):
        vectorstore = Chroma(
            persist_directory=DB_DIR, 
            embedding_function=embeddings
        )
        return vectorstore
    else:
        raise Exception(f"Database directory not found at {DB_DIR}")