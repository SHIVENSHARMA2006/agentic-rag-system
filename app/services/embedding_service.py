from app.providers.embeddings.google_embedding_provider import (
    GoogleEmbeddingProvider,
)


class EmbeddingService:

    def __init__(self):

        self.provider = GoogleEmbeddingProvider()

    def embed(self, text: str):

        return self.provider.generate_embedding(text)