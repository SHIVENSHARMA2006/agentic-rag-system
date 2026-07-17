from app.agents.state import GraphState
from app.providers.llm.google_llm_provider import (
    GoogleLLMProvider,
)


class AnswerAgent:
    """
    Generates the final response using the
    fused context and the user's question.
    """

    def __init__(self):
        self.llm = GoogleLLMProvider()

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        prompt = f"""
You are an intelligent AI assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context,
say that you don't have enough information.

Question:
{state["question"]}

Context:
{state["verified_context"]}

Answer:
"""

        answer = self.llm.generate(prompt)

        state["answer"] = answer

        return state