from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel


class Source(BaseModel):
    type: str
    title: str
    source: str
    score: Any = None


class AgentStepSummary(BaseModel):
    id: str
    label: str
    status: Literal["complete", "failed", "skipped"]
    duration_ms: int | None = None


class AgentRunMetrics(BaseModel):
    latency_ms: int
    retrieval_count: int
    web_result_count: int
    source_count: int
    context_characters: int


class AgentRunSummary(BaseModel):
    steps: list[AgentStepSummary]
    metrics: AgentRunMetrics


class ChatResponse(BaseModel):
    conversation_id: UUID
    conversation_title: str | None = None
    answer: str
    sources: list[Source]
    run: AgentRunSummary | None = None
