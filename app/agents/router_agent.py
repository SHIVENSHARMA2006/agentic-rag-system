from app.agents.base import BaseAgent
from app.agents.state import GraphState
from app.providers.llm.groq_llm_provider import GroqLLMProvider
from app.utils.json_parser import extract_json


PLANNING_PROMPT = """
You are an expert AI Planning & Routing Agent for an Agentic Retrieval-Augmented Generation (RAG) system.

Your job is NOT to answer the question.
Your sole responsibility is to evaluate the user's question and detected intent, and decide which information sources are needed to formulate the most complete and accurate response.

Available Information Sources:

1. Uploaded Documents (use_retrieval):
   - Internal knowledge base, private documents, uploaded PDFs, manuals, reports, meeting notes, resumes, or proprietary company files.
   - Use when the user explicitly or implicitly refers to their uploaded files, internal records, or domain-specific personal/company data.

2. Web Search (use_web):
   - Real-time events, sports scores, weather, breaking news, public knowledge, current officeholders, market data, and latest technology developments.
   - Use when the question asks about public facts, external entities, recent happenings, or broad topics unlikely to exist exclusively in user-uploaded documents.

Routing Rules:
- If the question specifically pertains to uploaded documents only:
  {{
      "use_retrieval": true,
      "use_web": false,
      "reason": "The query depends exclusively on internal uploaded documents."
  }}

- If the question requires external, public, factual, or real-time information:
  {{
      "use_retrieval": false,
      "use_web": true,
      "reason": "The query requires public external knowledge or current web information."
  }}

- If the question requires cross-referencing internal documents with external/web trends, or when broad context from both sources will yield a superior response:
  {{
      "use_retrieval": true,
      "use_web": true,
      "reason": "Comprehensive response requires both internal documents and external web knowledge."
  }}

- If the input is purely conversational (greeting, thanks, pleasantry):
  {{
      "use_retrieval": false,
      "use_web": false,
      "reason": "Purely conversational input requiring no external retrieval."
  }}

Examples:

Question: Summarize my uploaded resume.
Output:
{{
    "use_retrieval": true,
    "use_web": false,
    "reason": "Question pertains specifically to the user's uploaded resume."
}}

Question: Who won the FIFA World Cup 2022?
Output:
{{
    "use_retrieval": false,
    "use_web": true,
    "reason": "Public factual knowledge available on the web."
}}

Question: How does the revenue in our Q3 financial report compare to current industry market trends?
Output:
{{
    "use_retrieval": true,
    "use_web": true,
    "reason": "Requires internal financial report plus external market information from the web."
}}

Question: Hello, how can you help me?
Output:
{{
    "use_retrieval": false,
    "use_web": false,
    "reason": "Conversational greeting."
}}

Return ONLY valid JSON.

Question:
{question}

Detected Intent:
{intent}

Recent conversation (use it only to resolve what the latest question refers to):
{history}
"""


class RouterAgent(BaseAgent):

    def __init__(self):
        self.llm = GroqLLMProvider()

    def execute(
        self,
        state: GraphState,
    ) -> GraphState:

        prompt = PLANNING_PROMPT.format(
            question=state.get("standalone_question", state["question"]),
            intent=state["intent"],
            history="\n".join(
                f'{message["role"].title()}: {message["content"]}'
                for message in state.get("conversation_history", [])
            ) or "No earlier turns.",
        )

        response = self.llm.generate(prompt)

        print("\n========== ROUTER RAW RESPONSE ==========")
        print(response)
        print("=========================================\n")

        plan = extract_json(response)

        default_plan = {
            "use_retrieval": True,
            "use_web": False,
            "reason": "Fallback plan because planning failed.",
        }

        if not isinstance(plan, dict):
            plan = default_plan

        plan.setdefault("use_retrieval", True)
        plan.setdefault("use_web", False)
        plan.setdefault("reason", "")

        state["plan"] = plan

        return state
