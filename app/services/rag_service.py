from app.agents.graph import graph
from app.agents.state_factory import (
    create_initial_state,
)
from app.core.logging import logger


class RAGService:
    """
    Entry point for the complete Agentic RAG workflow.
    """

    def ask(
        self,
        question: str,
    ) -> dict:

        logger.info(
            "Starting Agentic RAG workflow..."
        )

        state = create_initial_state(
            question=question,
        )

        final_state = graph.invoke(
            state,
        )

        logger.info(
            "Workflow completed successfully."
        )

        return {
            "answer": final_state.get(
                "answer",
                "",
            ),
            "sources": final_state.get(
                "sources",
                [],
            ),
        }