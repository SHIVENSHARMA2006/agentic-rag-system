from app.agents.graph import graph
from app.agents.state_factory import create_initial_state
from app.core.logging import logger
from app.memory.chat_history import ConversationMessage


class RAGService:
    """
    Executes the complete Agentic RAG pipeline.
    """

    @staticmethod
    def _build_run_summary(final_state: dict) -> dict:
        metadata = final_state.get("metadata", {})
        timings = metadata.get("timings", {})
        services = metadata.get("services", {})
        warnings = metadata.get("warnings", [])
        failed_agents = {
            warning.split(":", 1)[0]
            for warning in warnings
            if isinstance(warning, str) and ":" in warning
        }

        pipeline = [
            ("query_understanding", "Query understanding", "QueryUnderstandingAgent", None),
            ("planning", "Planning", "RouterAgent", None),
            ("retrieval", "Document retrieval", "RetrievalAgent", "retrieval"),
            ("web_search", "Web search", "WebAgent", "web"),
            ("context_fusion", "Context fusion", "ContextFusionAgent", None),
            ("response", "Response generation", "ResponseAgent", None),
        ]
        steps = []
        for step_id, label, agent_name, service_name in pipeline:
            duration_seconds = timings.get(agent_name)
            if agent_name not in timings:
                status = "skipped"
            elif agent_name in failed_agents:
                status = "failed"
            elif service_name and services.get(service_name) is False:
                status = "skipped"
            else:
                status = "complete"

            steps.append({
                "id": step_id,
                "label": label,
                "status": status,
                "duration_ms": round(duration_seconds * 1000) if isinstance(duration_seconds, (int, float)) else None,
            })

        sources = final_state.get("sources", [])
        return {
            "steps": steps,
            "metrics": {
                "latency_ms": round(sum(
                    duration for duration in timings.values()
                    if isinstance(duration, (int, float))
                ) * 1000),
                "retrieval_count": metadata.get("document_chunks", 0),
                "web_result_count": metadata.get("web_results", 0),
                "source_count": len(sources),
                "context_characters": metadata.get("context_length", 0),
            },
        }

    def ask(
        self,
        question: str,
        conversation_history: list[ConversationMessage] | None = None,
    ) -> dict:

        logger.info(
            "Starting Agentic RAG workflow..."
        )

        try:

            state = create_initial_state(
                question=question,
                conversation_history=conversation_history,
            )

            final_state = graph.invoke(
                state,
            )

            logger.info(
                "Workflow completed successfully."
            )

            return {
                "conversation_title": final_state.get("conversation_title") or None,
                "answer": final_state.get(
                    "answer",
                    "",
                ),
                "sources": final_state.get(
                    "sources",
                    [],
                ),
                "run": self._build_run_summary(final_state),
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
