import asyncio
import json

from app.graph.workflow import graph


async def main():
    config = {
        "configurable": {
            "thread_id": "business-information-test-1"
        }
    }

    result = await graph.ainvoke(
        {
            "task": "Tesla'nın elektrikli araç pazarındaki başlıca rakipleri kimler?"
        },
        config=config,
    )

    print("\n--- BUSINESS INFORMATION GRAPH RESULT ---")
    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    asyncio.run(main())