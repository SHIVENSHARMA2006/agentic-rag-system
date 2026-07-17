from fastapi import APIRouter, Depends

from app.core.dependencies import (
    get_google_ai_service,
    get_qdrant_service,
)
from app.services.google_ai_service import GoogleAIService
from app.services.qdrant_service import QdrantService

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health(
    ai_service: GoogleAIService = Depends(get_google_ai_service),
    qdrant_service: QdrantService = Depends(get_qdrant_service),
):

    google_status = True
    google_error = None

    qdrant_status = True
    qdrant_error = None

    try:
        ai_service.health_check()
    except Exception as e:
        google_status = False
        google_error = str(e)

    try:
        qdrant_service.health_check()
    except Exception as e:
        qdrant_status = False
        qdrant_error = str(e)

    return {
        "backend": "healthy",
        "google_ai": google_status,
        "google_error": google_error,
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