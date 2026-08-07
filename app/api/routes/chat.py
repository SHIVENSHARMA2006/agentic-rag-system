from fastapi import APIRouter, HTTPException

from app.models.request_models import ChatRequest
from app.models.response_models import ChatResponse

from app.services.rag_service import RAGService

router = APIRouter(
    prefix="",
    tags=["Chat"],
)

rag = RAGService()


@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
):
    try:

        response = rag.ask(
            request.question
        )

        return response

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )