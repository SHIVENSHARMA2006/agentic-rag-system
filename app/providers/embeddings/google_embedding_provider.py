from google import genai

from app.core.settings import settings


class GoogleEmbeddingProvider:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GOOGLE_API_KEY,
        )

    def generate_embedding(self, text: str):
        response = self.client.models.embed_content(
            model=settings.EMBEDDING_MODEL,
            contents=text,
        )
        return response.embeddings[0].values

    def embed_query(self, query: str):
        return self.generate_embedding(query)

    def embed_document(self, text: str):
        return self.generate_embedding(text)

    def embedding_dimension(self):
        return len(self.generate_embedding("hello"))