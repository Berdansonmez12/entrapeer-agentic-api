import asyncio
import json

from app.graph.workflow import graph


async def main():
    config = {
        "configurable": {
            "thread_id": "code-agent-test-1"
        }
    }

    result = await graph.ainvoke(
        {
            "task": "Python ile bir dosyayı okuyup yazan kod yaz"
        },
        config=config,
    )

    print("\n--- CODE AGENT GRAPH RESULT ---")
    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
