from fastapi import HTTPException


class DocumentAlreadyExistsError(Exception):
    """Raised when the uploaded document already exists."""


class EmbeddingGenerationError(Exception):
    """Raised when embedding generation fails."""


class LLMProviderError(Exception):
    """Raised when the LLM provider fails."""


class VectorStoreError(Exception):
    """Raised when Qdrant operations fail."""


class DocumentExtractionError(Exception):
    """Raised when document parsing fails."""


def to_http_exception(exc: Exception):
    if isinstance(exc, DocumentAlreadyExistsError):
        return HTTPException(status_code=409, detail=str(exc))

    if isinstance(exc, DocumentExtractionError):
        return HTTPException(status_code=400, detail=str(exc))

    if isinstance(exc, EmbeddingGenerationError):
        return HTTPException(status_code=500, detail=str(exc))

    if isinstance(exc, VectorStoreError):
        return HTTPException(status_code=500, detail=str(exc))

    if isinstance(exc, LLMProviderError):
        return HTTPException(status_code=503, detail=str(exc))

    return HTTPException(status_code=500, detail="Internal Server Error")