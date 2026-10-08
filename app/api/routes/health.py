from fastapi import APIRouter, Depends

from app.core.dependencies import get_qdrant_service
from app.providers.llm.groq_llm_provider import GroqLLMProvider
from app.services.qdrant_service import QdrantService

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health(
    qdrant_service: QdrantService = Depends(get_qdrant_service),
):
    llm_status = True
    llm_error = None

    qdrant_status = True
    qdrant_error = None

    try:
        GroqLLMProvider().health_check()
    except Exception as e:
        llm_status = False
        llm_error = str(e)

    try:
        qdrant_service.health_check()
    except Exception as e:
        qdrant_status = False
        qdrant_error = str(e)

    return {
        "backend": "healthy" if llm_status and qdrant_status else "degraded",
        "llm_provider": "groq",
        "llm": llm_status,
        "llm_error": llm_error,
        "qdrant": qdrant_status,
        "qdrant_error": qdrant_error,
    }


@router.post("/initialize")
async def initialize(
    qdrant_service: QdrantService = Depends(get_qdrant_service),
):

    qdrant_service.create_collection()

    info = qdrant_service.get_collection_info()

    return {
        "status": "initialized",
        "collection": info.config.params.vectors,
    }
