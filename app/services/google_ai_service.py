from typing import List

from google import genai

from app.core.settings import settings


class GoogleAIService:
    """
    Central service responsible for all interactions
    with Google's AI models.

    Every future AI agent will use this service.
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GOOGLE_API_KEY
        )

    # -----------------------------
    # Chat Generation
    # -----------------------------
    def generate_response(
        self,
        prompt: str,
        model: str | None = None,
    ) -> str:

        model_name = model or settings.LLM_MODEL

        response = self.client.models.generate_content(
            model=model_name,
            contents=prompt,
        )

        return response.text

    # -----------------------------
    # Embeddings
    # -----------------------------
    def generate_embedding(
        self,
        text: str,
        model: str | None = None,
    ) -> List[float]:

        model_name = model or settings.EMBEDDING_MODEL

        response = self.client.models.embed_content(
            model=model_name,
            contents=text,
        )

        return response.embeddings[0].values

    # -----------------------------
    # Batch Embeddings
    # -----------------------------
    def generate_batch_embeddings(
        self,
        texts: List[str],
        model: str | None = None,
    ) -> List[List[float]]:

        model_name = model or settings.EMBEDDING_MODEL

        response = self.client.models.embed_content(
            model=model_name,
            contents=texts,
        )

        return [
            embedding.values
            for embedding in response.embeddings
        ]

    # -----------------------------
    # Health Check
    # -----------------------------
    def health_check(self):
     self.generate_response("Reply only with OK.")
     return True