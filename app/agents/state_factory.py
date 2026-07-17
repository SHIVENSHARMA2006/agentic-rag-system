from app.agents.state import GraphState


def create_initial_state(
    question: str,
) -> GraphState:
    """
    Creates the initial graph state.
    """

    return {
        "question": question,
        "intent": "",
        "plan": {},
        "retrieved_chunks": [],
        "web_results": [],
        "verified_context": "",
        "answer": "",
        "sources": [],
        "metadata": {},
    }