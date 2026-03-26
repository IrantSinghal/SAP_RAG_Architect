import os
import toml
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

def get_llm(groq_key):
    groq_key = os.environ.get("GROQ_API_KEY")
    if not groq_key:
        try:
            with open(".streamlit/secrets.toml", "r") as f:
                secrets = toml.load(f)
                groq_key = secrets.get("GROQ_API_KEY")
        except:
            pass
    
    if not groq_key:
        return None
    return ChatGroq(model_name="llama-3.3-70b-versatile", groq_api_key=groq_key, temperature=0.1)

system_prompt = """You are a Lead SAP Architect and Technical Assistant.
Your goal is to provide accurate, structured, and technical answers based ONLY on the provided context.

Rules:
1. If the user's question is a general greeting (like 'hi' or 'hello'), respond warmly without searching the documentation.
2. For technical questions, prioritize 'Clean Core' and SAP BTP best practices.
3. If the answer is not in the context, clearly state that the documentation does not contain sufficient information.

Context: {context}
Question: {question}"""

def get_prompt_template():
    return ChatPromptTemplate.from_template(system_prompt)
