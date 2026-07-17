from functools import lru_cache

from app.services.google_ai_service import GoogleAIService
from app.services.qdrant_service import QdrantService


@lru_cache
def get_google_ai_service():
    """
    Returns a singleton instance of GoogleAIService.
    """
    return GoogleAIService()


@lru_cache
def get_qdrant_service():
    """
    Returns a singleton instance of QdrantService.
    """
    return QdrantService()