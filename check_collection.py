from qdrant_client import QdrantClient
from app.core.settings import settings

client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
)

info = client.get_collection(settings.QDRANT_COLLECTION_NAME)

print(info)