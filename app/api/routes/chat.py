from fastapi import APIRouter, HTTPException
from uuid import uuid4

from app.models.request_models import ChatRequest
from app.models.response_models import ChatResponse

from app.services.rag_service import RAGService
from app.memory.chat_history import ChatHistoryStore

router = APIRouter(
    prefix="",
    tags=["Chat"],
)

rag = RAGService()
chat_history = ChatHistoryStore()


@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
):
    try:
        conversation_id = str(request.conversation_id or uuid4())
        history = chat_history.get_history(conversation_id)

        response = rag.ask(
            request.question,
            conversation_history=history,
        )

        response["conversation_id"] = conversation_id
        answer = response.get("answer", "")
        if answer and answer not in {
            "I couldn't find enough information to answer your question.",
            "Sorry, an unexpected error occurred while processing your request.",
        }:
            chat_history.append_turn(conversation_id, request.question, answer)

        return response

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
