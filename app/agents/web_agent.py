from app.agents.base import BaseAgent
from app.agents.state import GraphState
from app.services.tavily_service import TavilyService


class WebAgent(BaseAgent):

    def __init__(self):

        self.tavily = TavilyService()

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
            "use_web",
            False,
        ):

            metadata["services"][
                "web"
            ] = False

            state["web_results"] = []

            return state

        results = self.tavily.search(
            state["question"]
        )

        metadata["services"][
            "web"
        ] = True

        if not results:

            metadata["warnings"].append(
                "No web search results found."
            )

        state["web_results"] = results

        return state