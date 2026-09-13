from pydantic import BaseModel, Field


class ContentResult(BaseModel):
    content: str = Field(
        ...,
        description="The final written content produced for the user.",
    )
    content_type: str = Field(
        ...,
        description="The type of content produced, such as email, article, summary, or marketing copy.",
    )
    explanation: str = Field(
        ...,
        description="A concise explanation of the content approach.",
    )


class ContentAgent:
    """
    Specialized agent responsible for handling content creation
    and content transformation requests.
    """

    def __init__(self, llm):
        self.llm = llm

    async def execute(self, task: str) -> ContentResult:
        """
        Generate clear and task-focused written content.
        """
        structured_llm = self.llm.with_structured_output(ContentResult)

        system_prompt = """
        You are the Content Agent in a modular agentic system.

        Your responsibility is to handle requests that require creating,
        rewriting, summarizing, or improving written content.

        RULES:
        - Focus only on the content task provided by the user.
        - Follow the requested tone, format, audience, and language.
        - Keep the output clear, useful, and professional.
        - Do not perform business discovery.
        - Do not invent factual claims that are not provided by the user.
        - Do not ask unrelated questions.
        - If minor information is missing, make a reasonable minimal
          assumption and mention it briefly in the explanation.
        """

        messages = [
            ("system", system_prompt),
            ("human", task),
        ]

        return await structured_llm.ainvoke(messages)