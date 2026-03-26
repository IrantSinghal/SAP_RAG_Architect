
def get_retriever(vectorstore):
    return vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 7})

def generate_hypothetical_doc(llm, user_input, history_text):
    HYDE_PROMPT = """You are an SAP Documentation Architect.
Your task is to generate a 3-4 sentence hypothetical technical paragraph that directly answers the user's query.
This hypothetical document will be used for embedding search, so it should sound like official SAP documentation.
If the query is ambiguous (like 'assigning roles' or 'extensibility'), make sure to include technical details for BOTH SAP BTP and SAP S/4HANA.
Consider the chat history for context.

Chat History:
{history_text}

User Query: {user_input}

Hypothetical Document:"""

    try:
        hyde_formatted = HYDE_PROMPT.format(history_text=history_text, user_input=user_input)
        hypothetical_doc = llm.invoke(hyde_formatted).content.strip()
        return hypothetical_doc
    except Exception:
        return user_input

def get_context_and_docs(vectorstore, llm, user_input, history_text):
    if not vectorstore:
        return "", []
    
    hypothetical_doc = generate_hypothetical_doc(llm, user_input, history_text)
    retriever = get_retriever(vectorstore)
    retrieved_docs = retriever.invoke(hypothetical_doc)
    context = "\n\n".join([d.page_content for d in retrieved_docs])
    
    return context, retrieved_docs
