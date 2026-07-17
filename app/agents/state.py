from typing import Any, TypedDict


class GraphState(TypedDict):
    """
    Shared state passed between all LangGraph agents.
    """

    # User Input
    question: str

    # Query Understanding
    intent: str

    # Planning
    plan: dict[str, Any]

    # Retrieval
    retrieved_chunks: list

    # Web Search
    web_results: list

    # Context
    verified_context: str

    # Final Response
    answer: str

    # Sources returned to frontend
    sources: list

    # Runtime metadata
    metadata: dict[str, Any]