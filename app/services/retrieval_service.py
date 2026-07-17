from app.core.settings import settings
from app.providers.embeddings.google_embedding_provider import (
    GoogleEmbeddingProvider,
)
from app.repositories.vector_repository import VectorRepository


class RetrievalService:
    """
    Retrieves relevant chunks from Qdrant.
    """

    def __init__(self):

        self.embedding_provider = GoogleEmbeddingProvider()

        self.repository = VectorRepository()

    def retrieve(
        self,
        query: str,
        top_k: int = settings.TOP_K_RETRIEVAL,
    ) -> list:

        embedding = self.embedding_provider.embed_query(
            query
        )

        results = self.repository.search(
            embedding=embedding,
            limit=top_k,
        )

        chunks = []

        for point in results:

            payload = point["payload"]

            chunks.append(
                {
                    "type": "document",
                    "title": payload.get(
                        "filename",
                        "Uploaded Document",
                    ),
                    "content": payload["text"],
                    "source": payload.get(
                        "filename",
                        "Unknown",
                    ),
                    "score": point["score"],
                }
            )

        return chunks