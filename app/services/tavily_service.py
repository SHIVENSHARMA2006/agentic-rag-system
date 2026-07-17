from tavily import TavilyClient

from app.core.settings import settings


class TavilyService:
    """
    Wrapper around Tavily Search.
    """

    def __init__(self):

        self.client = TavilyClient(
            api_key=settings.TAVILY_API_KEY
        )

    def search(
        self,
        query: str,
        max_results: int = 3,
    ) -> list:

        response = self.client.search(
            query=query,
            max_results=max_results,
        )

        results = []

        for item in response.get(
            "results",
            [],
        ):

            results.append(
                {
                    "type": "web",
                    "title": item.get(
                        "title",
                        "",
                    ),
                    "content": item.get(
                        "content",
                        "",
                    ),
                    "source": item.get(
                        "url",
                        "",
                    ),
                    "score": None,
                }
            )

        return results