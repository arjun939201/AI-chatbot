from typing import Any

from tavily import TavilyClient

from backend.app.config import settings


class WebSearchService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = (
            TavilyClient(api_key=api_key)
            if api_key
            else None
        )

    def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[dict[str, Any]]:

        if not self.client:
            return []

        try:
            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=max_results,
                include_answer=False,
                include_raw_content=False,
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

        except Exception:
            return []


web_search_service = WebSearchService(
    settings.tavily_api_key
)
