from app.agents.base import BaseAgent
from app.agents.state import GraphState
from app.providers.llm.google_llm_provider import GoogleLLMProvider


QUERY_PROMPT = """
You are an expert Query Understanding Agent.

Classify the user's request.

Return ONLY one word.

Possible values:

information
comparison
summarization
analysis
greeting
other

Question:
{question}

Intent:
"""


class QueryUnderstandingAgent(BaseAgent):

    def __init__(self):

        self.llm = GoogleLLMProvider()

    def execute(
        self,
        state: GraphState,
    ) -> GraphState:

        response = self.llm.generate(
            QUERY_PROMPT.format(
                question=state["question"]
            )
        )

        intent = response.strip().lower()

        allowed = {
            "information",
            "comparison",
            "summarization",
            "analysis",
            "greeting",
            "other",
        }

        if intent not in allowed:

            intent = "information"

        state["intent"] = intent

        return state