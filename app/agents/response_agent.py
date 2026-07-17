from app.agents.base import BaseAgent
from app.agents.state import GraphState
from app.providers.llm.google_llm_provider import (
    GoogleLLMProvider,
)


SYSTEM_PROMPT = """
You are an intelligent AI assistant.

Answer the user's question using ONLY the provided context.

Rules:

1. Never invent information.
2. If the answer is unavailable, clearly say so.
3. If both uploaded documents and web search are present,
   combine them naturally.
4. Use bullet points when helpful.
5. Keep the answer concise but complete.
6. Never mention internal implementation details.

Question:

{question}

Context:

{context}

Answer:
"""


class ResponseAgent(BaseAgent):
    """
    Generates the final answer from the
    prepared context.
    """

    def __init__(self):

        self.llm = GoogleLLMProvider()

    def execute(
        self,
        state: GraphState,
    ) -> GraphState:

        context = state.get(
            "verified_context",
            "",
        ).strip()

        if not context:

            state["answer"] = (
                "I couldn't find enough information "
                "to answer your question."
            )

            return state

        prompt = SYSTEM_PROMPT.format(
            question=state["question"],
            context=context,
        )

        answer = self.llm.generate(
            prompt
        )

        state["answer"] = answer.strip()

        return state