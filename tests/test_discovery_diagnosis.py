from unittest.mock import AsyncMock, Mock

import pytest

from app.agents.discovery import (
    BusinessSenseDiscoveryAgent,
    DiscoveryDecision,
    DiscoveryHandoff,
    DiscoveryQuestion,
)
from app.agents.diagnosis import (
    DiagnosisResult,
    ProblemMainCause,
    ProblemSubCause,
    ProblemStructuringDiagnosisAgent,
    ProblemType,
)


@pytest.mark.asyncio
async def test_discovery_asks_question_before_minimum_three_questions():
    llm = Mock()
    agent = BusinessSenseDiscoveryAgent(llm)

    expected_result = DiscoveryDecision(
        is_discovery_complete=False,
        next_question=DiscoveryQuestion(
            question="Which customer segment is most affected?",
            purpose="Identify where the sales decline is concentrated.",
        ),
        handoff=None,
    )

    structured_llm = Mock()
    structured_llm.ainvoke = AsyncMock(return_value=expected_result)
    llm.with_structured_output.return_value = structured_llm

    conversation = [
        {
            "role": "user",
            "content": "Satışlarımız son 3 aydır düşüyor.",
        }
    ]

    result = await agent.discover(conversation)

    assert result.is_discovery_complete is False
    assert result.next_question is not None
    assert result.handoff is None


@pytest.mark.asyncio
async def test_discovery_guardrail_prevents_early_completion():
    llm = Mock()
    agent = BusinessSenseDiscoveryAgent(llm)

    premature_handoff = DiscoveryHandoff(
        customer_stated_problem="Sales are declining.",
        identified_business_problem="New customer conversion is declining.",
        hidden_root_risk="The true conversion bottleneck is still unclear.",
        customer_chat_summary="The customer reported a recent sales decline.",
    )

    model_result = DiscoveryDecision(
        is_discovery_complete=True,
        next_question=None,
        handoff=premature_handoff,
    )

    structured_llm = Mock()
    structured_llm.ainvoke = AsyncMock(return_value=model_result)
    llm.with_structured_output.return_value = structured_llm

    conversation = [
        {
            "role": "user",
            "content": "Satışlarımız düşüyor.",
        },
        {
            "role": "assistant",
            "content": "Düşüş hangi kanalda yoğunlaşıyor?",
        },
        {
            "role": "user",
            "content": "Online kanalda.",
        },
    ]

    result = await agent.discover(conversation)

    assert result.is_discovery_complete is False
    assert result.handoff is None
    assert result.next_question is not None


@pytest.mark.asyncio
async def test_discovery_allows_handoff_after_three_questions():
    llm = Mock()
    agent = BusinessSenseDiscoveryAgent(llm)

    expected_handoff = DiscoveryHandoff(
        customer_stated_problem="Sales have declined for three months.",
        identified_business_problem="New customer online conversion has declined.",
        hidden_root_risk="The conversion bottleneck may be deeper than traffic acquisition.",
        customer_chat_summary=(
            "Traffic is stable, but new customer add-to-cart and purchase "
            "conversion rates have declined."
        ),
    )

    model_result = DiscoveryDecision(
        is_discovery_complete=True,
        next_question=None,
        handoff=expected_handoff,
    )

    structured_llm = Mock()
    structured_llm.ainvoke = AsyncMock(return_value=model_result)
    llm.with_structured_output.return_value = structured_llm

    conversation = [
        {"role": "user", "content": "Satışlarımız düşüyor."},
        {"role": "assistant", "content": "Düşüş nerede yoğunlaşıyor?"},
        {"role": "user", "content": "Online ve yeni müşterilerde."},
        {"role": "assistant", "content": "Şu ana kadar ne denediniz?"},
        {"role": "user", "content": "Reklam bütçesini artırdık."},
        {"role": "assistant", "content": "Trafik ve dönüşüm nasıl değişti?"},
        {
            "role": "user",
            "content": "Trafik aynı ama dönüşüm oranı düştü.",
        },
    ]

    result = await agent.discover(conversation)

    assert result.is_discovery_complete is True
    assert result.handoff is not None
    assert result.handoff.identified_business_problem == (
        "New customer online conversion has declined."
    )


@pytest.mark.asyncio
async def test_diagnosis_returns_valid_problem_tree():
    llm = Mock()
    agent = ProblemStructuringDiagnosisAgent(llm)

    diagnosis = DiagnosisResult(
        problem_type=ProblemType.GROWTH,
        main_problem="New customer online conversion is declining.",
        main_causes=[
            ProblemMainCause(
                name="Customer acquisition quality",
                sub_causes=[
                    ProblemSubCause(
                        name="Audience mismatch",
                        explanation="Campaigns may attract low-intent visitors.",
                    ),
                    ProblemSubCause(
                        name="Channel mix",
                        explanation="Acquisition channels may not match target customers.",
                    ),
                ],
            ),
            ProblemMainCause(
                name="User experience",
                sub_causes=[
                    ProblemSubCause(
                        name="Product page friction",
                        explanation="Product pages may reduce add-to-cart behavior.",
                    ),
                    ProblemSubCause(
                        name="Navigation friction",
                        explanation="Users may struggle to find relevant products.",
                    ),
                ],
            ),
            ProblemMainCause(
                name="Checkout conversion",
                sub_causes=[
                    ProblemSubCause(
                        name="Payment friction",
                        explanation="Payment issues may increase abandonment.",
                    ),
                    ProblemSubCause(
                        name="Unexpected costs",
                        explanation="Additional costs may discourage purchase completion.",
                    ),
                ],
            ),
        ],
    )

    structured_llm = Mock()
    structured_llm.ainvoke = AsyncMock(return_value=diagnosis)
    llm.with_structured_output.return_value = structured_llm

    handoff = DiscoveryHandoff(
        customer_stated_problem="Sales are declining.",
        identified_business_problem="New customer online conversion is declining.",
        hidden_root_risk="The actual conversion bottleneck is unknown.",
        customer_chat_summary="Traffic is stable while conversion is declining.",
    )

    result = await agent.diagnose(handoff.model_dump())

    assert result.problem_type == ProblemType.GROWTH
    assert len(result.main_causes) == 3

    for main_cause in result.main_causes:
        assert 2 <= len(main_cause.sub_causes) <= 3