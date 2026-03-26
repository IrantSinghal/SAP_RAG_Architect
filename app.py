import os
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# We do NOT import heavy AI logic at the top level anymore. 
# This prevents Vercel from killing the app during the 10-second "Cold Start".

app = FastAPI()

# Global variables to hold our "Brain" once loaded
vectorstore = None
llm = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "SAP Architect API is Online", "mode": "Lazy-Loading"}

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.post("/chat")
async def chat_endpoint(request: Request):
    global vectorstore, llm
    
    # 🧠 STRATEGIC STEP: Lazy Initialization
    # If this is the first request, load the heavy models now.
    if vectorstore is None or llm is None:
        try:
            print("Vercel Cold Start: Loading SAP Knowledge Base...")
            from processor import initialize_knowledge_base
            from llm_utils import get_llm
            
            api_key = os.environ.get("GROQ_API_KEY")
            vectorstore = initialize_knowledge_base()
            llm = get_llm(api_key)
            print("Initialization Complete.")
        except Exception as e:
            return JSONResponse(status_code=500, content={"answer": f"Initialization Error: {str(e)}"})

    try:
        data = await request.json()
        user_query = data.get("query")
        history = data.get("history", [])

        # Format History (last 3 turns)
        history_text = "\n".join([f"User: {h['user']}\nAI: {h['ai']}" for h in history[-3:]])

        # HyDE & Retrieval
        from retriever import generate_hypothetical_doc 
        hyde_query = generate_hypothetical_doc(llm, user_query, history_text)
        docs = vectorstore.similarity_search(hyde_query, k=3)
        context = "\n".join([d.page_content for d in docs])
        
        # Final Generation
        system_msg = "You are a Lead SAP Architect. Use the provided context and history to answer."
        full_prompt = f"{system_msg}\n\nContext:\n{context}\n\nHistory:\n{history_text}\n\nQuestion: {user_query}"
        
        response = llm.invoke(full_prompt)
        return {"answer": response.content}

    except Exception as e:
        print(f"Runtime Error: {e}")
        return JSONResponse(status_code=500, content={"answer": f"Architectural Error: {str(e)}"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)