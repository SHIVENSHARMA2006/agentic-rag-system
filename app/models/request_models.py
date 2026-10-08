from pydantic import BaseModel, Field
from uuid import UUID


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="User question",
    )
    conversation_id: UUID | None = Field(
        default=None,
        description="Conversation ID used to retrieve recent chat history. A new one is created when omitted.",
    )
