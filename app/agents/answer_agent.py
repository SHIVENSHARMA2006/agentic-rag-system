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
You are an expert AI Research & Knowledge Synthesis Assistant.

Generate a comprehensive, highly accurate, and well-structured answer to the user's question, strictly grounded in the provided context.

Guidelines:
1. Grounding & Accuracy: Base your answer strictly on the provided context. Never hallucinate facts or extrapolate unverified details. If information is missing, state so clearly.
2. Structure & Formatting: Use clean Markdown with clear headings (e.g., ## Overview, ## Details, ## Key Takeaways), structured bullet points, and bold key terms.
3. Depth: Provide an in-depth and substantive response covering all relevant details rather than a brief summary.
4. Synthesis: Combine uploaded document data and web search results smoothly into a cohesive narrative.

Question:
{state["question"]}

Context:
{state["verified_context"]}

Answer:
"""

        answer = self.llm.generate(prompt)

        state["answer"] = answer

        return state