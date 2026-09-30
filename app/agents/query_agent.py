from app.agents.base import BaseAgent
from app.agents.state import GraphState
from app.providers.llm.google_llm_provider import GoogleLLMProvider


QUERY_PROMPT = """
You are an expert Query Understanding Agent in an advanced Agentic RAG system.

Analyze the user's question and accurately classify the primary user intent into exactly ONE category.

Allowed Categories:
- information: The user is looking for factual knowledge, specific details, background data, entity descriptions, or current events (e.g., "What is...", "Who is...", "When did...").
- comparison: The user wants to compare, contrast, or evaluate differences and similarities between two or more concepts, tools, or documents (e.g., "Compare X and Y", "How does A differ from B?").
- summarization: The user wants a summary, high-level overview, synopsis, or condensed extraction of a document or topic (e.g., "Summarize this document", "Give me the TL;DR of...").
- analysis: The user wants in-depth reasoning, root-cause investigation, pros/cons breakdown, impact evaluation, or technical assessment (e.g., "Why did X happen and what are the implications?", "Analyze the architecture of...").
- greeting: Conversational pleasantries, introductions, or system check-ins without a task (e.g., "Hello", "Hi there", "Good morning").
- other: Ambiguous, malformed, or general inputs that do not fit the above categories.

Rules:
1. Return ONLY the single matching intent category name from the list above.
2. Return it as ONE word in lowercase.
3. Do NOT include markdown, punctuation, quotation marks, or explanations.

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