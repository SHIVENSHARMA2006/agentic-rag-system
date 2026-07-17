from app.agents.base import BaseAgent
from app.agents.state import GraphState
from app.providers.llm.google_llm_provider import GoogleLLMProvider
from app.utils.json_parser import extract_json


PLANNING_PROMPT = """
You are an AI Planning Agent for an Agentic Retrieval-Augmented Generation (RAG) system.

Your job is NOT to answer the question.

Your only job is to decide which information source(s) are required.

Available sources:

1. Uploaded Documents
- PDFs
- Manuals
- Reports
- Notes
- Resumes
- Internal company knowledge

2. Web Search
- Current events
- Sports
- Weather
- News
- Public knowledge
- Recent developments
- Live information
- Information that is unlikely to exist in uploaded documents

Use these rules:

• If the answer should come ONLY from uploaded documents:

{{
    "use_retrieval": true,
    "use_web": false,
    "reason": "..."
}}

• If the answer requires ONLY public/current information:

{{
    "use_retrieval": false,
    "use_web": true,
    "reason": "..."
}}

• If both sources are needed:

{{
    "use_retrieval": true,
    "use_web": true,
    "reason": "..."
}}

Examples

Question:
Summarize my uploaded resume.

Output:
{{
    "use_retrieval": true,
    "use_web": false,
    "reason": "The answer depends entirely on uploaded documents."
}}

Question:
Who won FIFA World Cup 2022?

Output:
{{
    "use_retrieval": false,
    "use_web": true,
    "reason": "This is public factual information."
}}

Question:
Compare my uploaded AI report with today's AI news.

Output:
{{
    "use_retrieval": true,
    "use_web": true,
    "reason": "Comparison requires both uploaded documents and recent web information."
}}

Question:
What is today's weather in Delhi?

Output:
{{
    "use_retrieval": false,
    "use_web": true,
    "reason": "Weather is real-time information."
}}

Return ONLY valid JSON.

Question:
{question}

Detected Intent:
{intent}
"""


class RouterAgent(BaseAgent):

    def __init__(self):
        self.llm = GoogleLLMProvider()

    def execute(
        self,
        state: GraphState,
    ) -> GraphState:

        prompt = PLANNING_PROMPT.format(
            question=state["question"],
            intent=state["intent"],
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