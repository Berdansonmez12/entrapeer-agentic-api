import asyncio

from app.services.web_search_service import WebSearchService


async def main():
    service = WebSearchService()

    results = await service.search(
        "Tesla main competitors electric vehicle market 2026",
        max_results=3,
    )

    print("\n--- WEB SEARCH RESULTS ---")

    for index, result in enumerate(results, start=1):
        print(f"\nRESULT {index}")
        print("Title:", result["title"])
        print("URL:", result["url"])
        print("Content:", result["content"][:300])


if __name__ == "__main__":
    asyncio.run(main())