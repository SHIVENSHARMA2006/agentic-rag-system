from app.agents.graph import graph
from app.agents.state_factory import create_initial_state
from app.core.logging import logger


class RAGService:
    """
    Executes the complete Agentic RAG pipeline.
    """

    def ask(
        self,
        question: str,
    ) -> dict:

        logger.info(
            "Starting Agentic RAG workflow..."
        )

        try:

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

        except Exception as e:

            logger.exception(e)

            return {
                "answer": (
                    "Sorry, an unexpected error occurred "
                    "while processing your request."
                ),
                "sources": [],
            }