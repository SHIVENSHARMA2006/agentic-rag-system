from google import genai
from google.genai import types

from app.core.settings import settings
from app.core.exceptions import LLMProviderError
from app.providers.llm.base import BaseLLMProvider


class GoogleLLMProvider(BaseLLMProvider):
    """
    Google Gemini implementation of our LLM Provider.
    """

    def __init__(self):
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)

    def generate(self, prompt: str) -> str:
        """
        Generate a response using Gemini.
        """

        try:
            response = self.client.models.generate_content(
                model=settings.LLM_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2
                ),
            )

            return response.text

        except Exception as e:
            raise LLMProviderError(str(e))

    def health_check(self) -> bool:
        """
        Basic provider health check.
        """

        try:
            self.generate("Reply only with OK.")
            return True

        except Exception:
            return False