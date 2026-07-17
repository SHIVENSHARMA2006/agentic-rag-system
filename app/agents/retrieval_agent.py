from app.agents.base import BaseAgent
from app.agents.state import GraphState
from app.services.retrieval_service import RetrievalService


class RetrievalAgent(BaseAgent):

    def __init__(self):

        self.retrieval_service = RetrievalService()

    def execute(
        self,
        state: GraphState,
    ) -> GraphState:

        metadata = state["metadata"]

        plan = state.get(
            "plan",
            {},
        )

        if not plan.get(
            "use_retrieval",
            False,
        ):

            metadata["services"][
                "retrieval"
            ] = False

            state["retrieved_chunks"] = []

            return state

        chunks = self.retrieval_service.retrieve(
            state["question"]
        )

        metadata["services"][
            "retrieval"
        ] = True

        if not chunks:

            metadata["warnings"].append(
                "No relevant document chunks found."
            )

        state["retrieved_chunks"] = chunks

        return state