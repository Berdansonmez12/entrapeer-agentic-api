import asyncio
import json

from app.agents.business_information import BusinessInformationAgent
from app.services.llm_service import LLMService
from app.services.web_search_service import WebSearchService


async def main():
    task = "Tesla'nın elektrikli araç pazarındaki başlıca rakipleri kimler?"

    # 1. Search the web for current business information.
    search_service = WebSearchService()
    search_results = await search_service.search(
        query=task,
        max_results=5,
    )

    # 2. Convert search results into context for the LLM.
    web_context = "\n\n".join(
        [
            (
                f"Title: {result['title']}\n"
                f"URL: {result['url']}\n"
                f"Content: {result['content']}"
            )
            for result in search_results
        ]
    )

    sources = [
        {
            "title": result["title"],
            "url": result["url"],
        }
        for result in search_results
    ]

    # 3. Generate a grounded business answer.
    llm = LLMService().get_model()
    agent = BusinessInformationAgent(llm)

    result = await agent.answer(
        task=task,
        web_context=web_context,
        sources=sources,
    )

    print("\n--- BUSINESS INFORMATION RESULT ---")
    print(
        json.dumps(
            result.model_dump(),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    asyncio.run(main())