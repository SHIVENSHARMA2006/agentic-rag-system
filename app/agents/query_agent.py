from app.agents.base import BaseAgent
from app.agents.state import GraphState
from app.providers.llm.groq_llm_provider import GroqLLMProvider
from app.utils.json_parser import extract_json


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
1. Classify the latest user message into exactly ONE allowed intent.
2. Rewrite the latest message as a standalone question by resolving references from recent conversation. If it is already standalone or there is no prior conversation, keep its meaning unchanged.
3. Do not answer the question or add facts that were not in the user's message/history.
4. Create a concise, descriptive, title-cased chat title of at most six words, based on the conversation's main topic. Do not repeat the user's full question or include question wording such as "What is" or "How does". Avoid generic titles such as "New Chat".
5. Return ONLY valid JSON with exactly these keys: "intent", "standalone_question", and "conversation_title".

Question:
{question}

Recent conversation (for understanding follow-up references):
{history}

JSON:
"""


class QueryUnderstandingAgent(BaseAgent):

    def __init__(self):

        self.llm = GroqLLMProvider()

    def execute(
        self,
        state: GraphState,
    ) -> GraphState:

        response = self.llm.generate(
            QUERY_PROMPT.format(
                question=state["question"],
                history="\n".join(
                    f'{message["role"].title()}: {message["content"]}'
                    for message in state.get("conversation_history", [])
                ) or "No earlier turns.",
            )
        )

        parsed = extract_json(response)
        intent = str(parsed.get("intent", response)).strip().lower()

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
        standalone_question = parsed.get("standalone_question")
        if isinstance(standalone_question, str) and standalone_question.strip():
            state["standalone_question"] = standalone_question.strip()
        conversation_title = parsed.get("conversation_title")
        if isinstance(conversation_title, str) and conversation_title.strip():
            state["conversation_title"] = conversation_title.strip()[:80]

        return state
