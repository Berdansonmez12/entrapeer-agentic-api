import asyncio
import json

from app.graph.workflow import graph


async def main():
    config = {
        "configurable": {
            "thread_id": "non-business-test-1"
        }
    }

    result = await graph.ainvoke(
        {
            "task": "Dünyanın en yüksek dağı hangisidir?"
        },
        config=config,
    )

    print("\n--- NON-BUSINESS GRAPH RESULT ---")
    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    asyncio.run(main())