from typing import List
import httpx

from app.core.logging import logger
from app.core.settings import settings
from app.providers.embeddings.google_embedding_provider import (
    GoogleEmbeddingProvider,
)


class VectorRepository:

    def __init__(self):

        self.base_url = settings.QDRANT_URL.rstrip("/")
        self.collection = settings.QDRANT_COLLECTION_NAME

        self.headers = {
            "api-key": settings.QDRANT_API_KEY,
            "Content-Type": "application/json",
        }

        provider = GoogleEmbeddingProvider()
        self.dimension = provider.embedding_dimension()

        self.client = httpx.Client(
            timeout=60,
        )

        self._ensure_collection()

    def _get(self, endpoint: str):

        response = self.client.get(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
        )

        response.raise_for_status()
        return response.json()

    def _put(self, endpoint: str, body: dict):

        response = self.client.put(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            json=body,
        )

        response.raise_for_status()
        return response.json()

    def _post(self, endpoint: str, body: dict):

        response = self.client.post(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            json=body,
        )

        response.raise_for_status()
        return response.json()

    def _ensure_collection(self):

        response = self._get("/collections")

        existing = {
            c["name"]
            for c in response["result"]["collections"]
        }

        if self.collection in existing:

            logger.info(
                f"Collection '{self.collection}' already exists."
            )
            return

        logger.info(
            f"Creating collection '{self.collection}'..."
        )

        body = {
            "vectors": {
                "size": self.dimension,
                "distance": "Cosine",
            }
        }

        self._put(
            f"/collections/{self.collection}",
            body,
        )

        logger.success("Collection created successfully.")

    def insert_batch(
        self,
        points: List,
    ):

        if not points:
            return

        formatted_points = []

        for point in points:

            formatted_points.append(
                {
                    "id": point.id,
                    "vector": point.vector,
                    "payload": point.payload,
                }
            )

        body = {
            "points": formatted_points,
        }

        self._put(
            f"/collections/{self.collection}/points?wait=true",
            body,
        )

    def search(
        self,
        embedding: list[float],
        limit: int = 5,
    ):

        body = {
            "vector": embedding,
            "limit": limit,
            "with_payload": True,
            "with_vector": False,
        }

        response = self._post(
            f"/collections/{self.collection}/points/search",
            body,
        )

        return response["result"]

    def health_check(self):

        return self._get("/collections")