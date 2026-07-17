from app.agents.graph import graph

state = {
    "question": "Explain Agentic RAG",

    "intent": "",

    "needs_retrieval": False,

    "needs_web_search": False,

    "retrieved_chunks": [],

    "web_results": [],

    "verified_context": "",

    "answer": "",
}

result = graph.invoke(state)

print(result)