from langgraph.graph import (
    END,
    StateGraph,
)

from app.agents.context_fusion_agent import ContextFusionAgent
from app.agents.query_agent import QueryUnderstandingAgent
from app.agents.response_agent import ResponseAgent
from app.agents.retrieval_agent import RetrievalAgent
from app.agents.router_agent import RouterAgent
from app.agents.state import GraphState
from app.agents.web_agent import WebAgent


builder = StateGraph(GraphState)

query_agent = QueryUnderstandingAgent()
router_agent = RouterAgent()
retrieval_agent = RetrievalAgent()
web_agent = WebAgent()
fusion_agent = ContextFusionAgent()
response_agent = ResponseAgent()


builder.add_node(
    "query_understanding",
    query_agent.run,
)

builder.add_node(
    "planning",
    router_agent.run,
)

builder.add_node(
    "retrieval",
    retrieval_agent.run,
)

builder.add_node(
    "web_search",
    web_agent.run,
)

builder.add_node(
    "context_fusion",
    fusion_agent.run,
)

builder.add_node(
    "response",
    response_agent.run,
)


builder.set_entry_point(
    "query_understanding",
)


builder.add_edge(
    "query_understanding",
    "planning",
)

builder.add_edge(
    "planning",
    "retrieval",
)

builder.add_edge(
    "retrieval",
    "web_search",
)

builder.add_edge(
    "web_search",
    "context_fusion",
)

builder.add_edge(
    "context_fusion",
    "response",
)

builder.add_edge(
    "response",
    END,
)


graph = builder.compile()