from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from processor import initialize_knowledge_base
# ✅ Use your actual filenames:
from llm_utils import get_llm 
from retriever import generate_hypothetical_doc # This matches your retriever.py
import uvicorn
from fastapi.responses import FileResponse

app = FastAPI()
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")
# Allow your HTML file to talk to this Python server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Components once
vectorstore = initialize_knowledge_base()
llm = get_llm("YOUR_GROQ_API_KEY")

@app.post("/chat")
async def chat_endpoint(request: Request):
    try:
        # 1. Parse incoming JSON
        data = await request.json()
        user_query = data.get("query")
        history = data.get("history", [])

        # 2. Format History (taking last 3 turns to stay efficient)
        history_text = "\n".join([f"User: {h['user']}\nAI: {h['ai']}" for h in history[-3:]])

        # 3. HyDE Query Expansion (Using history for better context)
        # Assuming generate_hypothetical_doc is imported from retriever.py
        hyde_query = generate_hypothetical_doc(llm, user_query, history_text)
        
        # 4. Retrieval from ChromaDB
        # Ensure vectorstore is initialized globally or inside this function
        docs = vectorstore.similarity_search(hyde_query, k=3)
        context = "\n".join([d.page_content for d in docs])
        
        # 5. Final Prompt Construction
        system_msg = "You are a Lead SAP Architect. Use the provided context and history to answer."
        full_prompt = f"{system_msg}\n\nContext:\n{context}\n\nHistory:\n{history_text}\n\nQuestion: {user_query}"
        
        # 6. LLM Call
        response = llm.invoke(full_prompt)
        
        # 7. Single Return Statement at the end
        return {"answer": response.content}

    except Exception as e:
        print(f"Backend Error: {e}") # Log to terminal for debugging
        return {"answer": f"Architectural Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)