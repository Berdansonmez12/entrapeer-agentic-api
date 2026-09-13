from tavily import AsyncTavilyClient

from app.core.config import get_settings


class WebSearchService:
    """
    Service responsible for retrieving current web information
    and returning normalized search results for business agents.
    """

    def __init__(self):
        settings = get_settings()

        if not settings.tavily_api_key:
            raise ValueError("TAVILY_API_KEY is not configured.")

        self.client = AsyncTavilyClient(
            api_key=settings.tavily_api_key
        )

    async def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[dict[str, str]]:
        """
        Search the web and return normalized source information.
        """
        response = await self.client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
            include_answer=False,
        )

        results = []

        for item in response.get("results", []):
            results.append(
                {
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "content": item.get("content", ""),
                }
            )

        return results