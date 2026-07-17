from app.agents.base import BaseAgent
from app.agents.state import GraphState
from app.core.settings import settings


class ContextFusionAgent(BaseAgent):
    """
    Combines retrieved document chunks and web search
    results into a single context while respecting the
    configured context budget.
    """

    def execute(
        self,
        state: GraphState,
    ) -> GraphState:

        metadata = state["metadata"]

        context_parts = []

        sources = []

        current_length = 0

        # -----------------------------
        # Uploaded Documents
        # -----------------------------

        document_chunks = state.get(
            "retrieved_chunks",
            [],
        )[: settings.MAX_RETRIEVAL_CHUNKS]

        if document_chunks:

            context_parts.append(
                "===== Uploaded Documents ====="
            )

            for chunk in document_chunks:

                content = chunk["content"][
                    : settings.MAX_CHUNK_LENGTH
                ]

                if (
                    current_length + len(content)
                    > settings.MAX_CONTEXT_LENGTH
                ):
                    break

                context_parts.append(
                    f"""Source: {chunk["source"]}

{content}
"""
                )

                current_length += len(content)

                sources.append(
                    {
                        "type": chunk["type"],
                        "title": chunk["title"],
                        "source": chunk["source"],
                        "score": chunk["score"],
                    }
                )

        # -----------------------------
        # Web Results
        # -----------------------------

        web_results = state.get(
            "web_results",
            [],
        )[: settings.MAX_WEB_RESULTS]

        if web_results:

            context_parts.append(
                "===== Web Search Results ====="
            )

            for result in web_results:

                content = result["content"][
                    : settings.MAX_WEB_CONTENT_LENGTH
                ]

                section = f"""
Title: {result["title"]}

Source: {result["source"]}

{content}
"""

                if (
                    current_length + len(section)
                    > settings.MAX_CONTEXT_LENGTH
                ):
                    break

                context_parts.append(section)

                current_length += len(section)

                sources.append(
                    {
                        "type": result["type"],
                        "title": result["title"],
                        "source": result["source"],
                        "score": None,
                    }
                )

        state["verified_context"] = "\n\n".join(
            context_parts
        )

        state["sources"] = sources

        metadata["context_length"] = current_length

        metadata["document_chunks"] = len(document_chunks)

        metadata["web_results"] = len(web_results)

        return state