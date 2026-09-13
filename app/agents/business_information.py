from pydantic import BaseModel, Field


class BusinessSource(BaseModel):
    title: str = Field(
        ...,
        description="Title of the source used in the business answer.",
    )
    url: str = Field(
        ...,
        description="URL of the source.",
    )


class BusinessInformationResult(BaseModel):
    answer: str = Field(
        ...,
        description="A concise and structured answer to the business question.",
    )
    sources: list[BusinessSource] = Field(
        default_factory=list,
        description="Reliable sources supporting the answer.",
    )


class BusinessInformationAgent:
    """
    Agent responsible for answering business information requests
    using current information retrieved from the web.
    """

    def __init__(self, llm):
        self.llm = llm

    async def answer(
        self,
        task: str,
        web_context: str,
        sources: list[dict[str, str]],
    ) -> BusinessInformationResult:
        """
        Produce a concise business answer grounded in retrieved web sources.
        """
        structured_llm = self.llm.with_structured_output(
            BusinessInformationResult
        )

        system_prompt = """
        You are the Business Information Agent in a business-focused
        agentic system.

        Your responsibility is to answer business information requests
        using the web research context provided to you.

        Typical requests include:
        - competitor information
        - company information
        - sector information
        - market trends

        RULES:
        - Use only information supported by the provided web research.
        - Do not invent facts or sources.
        - Do not start a discovery conversation.
        - Do not ask the customer discovery questions.
        - Keep the answer concise, clear, and business-focused.
        - Prefer reliable and current information.
        - Structure the answer so it is easy to read.
        - Include the relevant sources supplied in the research context.
        """

        messages = [
            ("system", system_prompt),
            (
                "human",
                f"""
Business question:
{task}

Web research:
{web_context}

Available sources:
{sources}

Answer the business question using this research.
""",
            ),
        ]

        return await structured_llm.ainvoke(messages)