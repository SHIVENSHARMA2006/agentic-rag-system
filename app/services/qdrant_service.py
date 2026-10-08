from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from app.core.settings import settings

print("QDRANT URL:", settings.QDRANT_URL)
print("API KEY LOADED:", bool(settings.QDRANT_API_KEY))

class QdrantService:
    """
    Central service responsible for all interactions
    with Qdrant.
    """

    # gemini-embedding-001 currently returns 3072-dimensional vectors.
    # Keep newly created collections compatible with the active embedding model.
    VECTOR_SIZE = 3072

    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
        )

        self.collection_name = settings.QDRANT_COLLECTION_NAME

    def create_collection(self):
        """
        Creates the collection only if it
        does not already exist.
        """

        collections = self.client.get_collections()

        existing = [
            collection.name
            for collection in collections.collections
        ]

        if self.collection_name in existing:
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

    def get_collection_info(self):
        return self.client.get_collection(
            self.collection_name
        )

    def health_check(self):
     try:
        collections = self.client.get_collections()
        print("Qdrant Connected Successfully!")
        print(collections)
        return True

     except Exception as e:
        print("\n========== QDRANT ERROR ==========")
        print(type(e))
        print(e)
        print("==================================\n")
        return False
