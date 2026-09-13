import asyncio
import json

from app.graph.workflow import graph


async def main():
    config = {
        "configurable": {
            "thread_id": "content-agent-test-1"
        }
    }

    result = await graph.ainvoke(
        {
            "task": "Yeni ürünümüz için kısa ve profesyonel bir tanıtım yazısı yaz"
        },
        config=config,
    )

    print("\n--- CONTENT AGENT GRAPH RESULT ---")
    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    asyncio.run(main())