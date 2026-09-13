import asyncio
import json

from app.graph.workflow import graph


async def main():
    config = {
        "configurable": {
            "thread_id": "discovery-test-1",
        }
    }

    first_result = await graph.ainvoke(
        {
            "task": "Satışlarımız son 3 aydır düşüyor.",
        },
        config=config,
    )

    print("\n--- FIRST TURN ---")
    print(json.dumps(first_result, ensure_ascii=False, indent=2))

    second_result = await graph.ainvoke(
        {
            "task": "Özellikle online kanalda ve yeni müşterilerde düşüş görüyoruz.",
        },
        config=config,
    )

    print("\n--- SECOND TURN ---")
    print(json.dumps(second_result, ensure_ascii=False, indent=2))


    third_result = await graph.ainvoke(
    {
        "task": "Online reklam bütçesini artırdık ve yeni müşterilere indirim verdik ama satışlarda belirgin bir iyileşme olmadı.",
    },
    config=config,
    )

    print("\n--- THIRD TURN ---")
    print(json.dumps(third_result, ensure_ascii=False, indent=2))


    fourth_result = await graph.ainvoke(
    {
        "task": "Trafik aslında düşmedi. Ziyaretçi sayımız benzer ama yeni müşterilerin sepete ürün ekleme ve satın alma oranları düştü. Öncelikli beklentimiz bu düşüşün kök nedenini anlamak.",
    },
    config=config,
)

    print("\n--- FOURTH TURN ---")
    print(json.dumps(fourth_result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())