import pytest

from app.agents.peer import (
    PeerAgent,
    PeerRoutingDecision,
    TaskRoute,
)


class FakeStructuredLLM:
    def __init__(self, decision: PeerRoutingDecision):
        self.decision = decision

    async def ainvoke(self, messages):
        return self.decision


class FakeLLM:
    def __init__(self, decision: PeerRoutingDecision):
        self.decision = decision

    def with_structured_output(self, schema):
        return FakeStructuredLLM(self.decision)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("expected_route", "task"),
    [
        (
            TaskRoute.BUSINESS_PROBLEM,
            "Satışlarımız son üç aydır düşüyor.",
        ),
        (
            TaskRoute.BUSINESS_INFORMATION,
            "Tesla'nın en büyük rakipleri kimler?",
        ),
        (
            TaskRoute.CODE,
            "Python ile bir dosyayı okuyup yazan kod yaz.",
        ),
        (
            TaskRoute.CONTENT,
            "Yeni ürünümüz için kısa bir tanıtım yazısı yaz.",
        ),
        (
            TaskRoute.NON_BUSINESS,
            "Dünyanın en yüksek dağı hangisidir?",
        ),
    ],
)
async def test_peer_agent_returns_structured_route(
    expected_route: TaskRoute,
    task: str,
):
    decision = PeerRoutingDecision(
        route=expected_route,
        reasoning="Test routing decision.",
    )

    peer_agent = PeerAgent(FakeLLM(decision))

    result = await peer_agent.classify(task)

    assert result.route == expected_route
    assert result.reasoning == "Test routing decision."