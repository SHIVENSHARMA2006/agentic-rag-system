from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI, RateLimitError

from app.core.exceptions import LLMProviderError
from app.core.settings import settings
from app.providers.llm.base import BaseLLMProvider


class GroqLLMProvider(BaseLLMProvider):
    """Text generation through Groq's OpenAI-compatible API."""

    def __init__(self):
        self.client: OpenAI | None = None

    def _get_client(self) -> OpenAI:
        if not settings.GROQ_API_KEY.strip():
            raise LLMProviderError(
                "GROQ_API_KEY is not configured. Add your Groq API key to the backend .env file."
            )

        if self.client is None:
            self.client = OpenAI(
                api_key=settings.GROQ_API_KEY,
                base_url="https://api.groq.com/openai/v1",
                max_retries=0,
            )
        return self.client

    def generate(self, prompt: str) -> str:
        try:
            response = self._get_client().chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            content = response.choices[0].message.content
            if not isinstance(content, str) or not content.strip():
                raise LLMProviderError("Groq returned an empty response.")
            return content.strip()
        except LLMProviderError:
            raise
        except RateLimitError as exc:
            raise LLMProviderError(f"Groq quota or rate limit reached: {exc}") from exc
        except APIStatusError as exc:
            raise LLMProviderError(
                f"Groq API request failed ({exc.status_code}): {exc.message}"
            ) from exc
        except (APIConnectionError, APITimeoutError) as exc:
            raise LLMProviderError(f"Could not connect to Groq: {exc}") from exc
        except Exception as exc:
            raise LLMProviderError(f"Groq request failed: {exc}") from exc

    def health_check(self) -> bool:
        self.generate("Reply only with OK.")
        return True
