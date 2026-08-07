from typing import Any

from pydantic import BaseModel


class Source(BaseModel):
    type: str
    title: str
    source: str
    score: Any = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]