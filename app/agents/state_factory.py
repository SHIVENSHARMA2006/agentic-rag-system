from app.agents.state import GraphState
from app.memory.chat_history import ConversationMessage


def create_initial_state(
    question: str,
    conversation_history: list[ConversationMessage] | None = None,
) -> GraphState:
    """
    Creates the initial graph state.
    """

    return {
        "question": question,
        "standalone_question": question,
        "conversation_title": "",
        "conversation_history": conversation_history or [],
        "intent": "",
        "plan": {},
        "retrieved_chunks": [],
        "web_results": [],
        "verified_context": "",
        "answer": "",
        "sources": [],
        "metadata": {},
    }
