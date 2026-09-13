from pydantic import BaseModel, Field


class CodeResult(BaseModel):
    explanation: str = Field(
        ...,
        description="A concise explanation of the generated code.",
    )
    code: str = Field(
        ...,
        description="The generated code that solves the user's request.",
    )
    language: str = Field(
        ...,
        description="The programming language used in the generated code.",
    )


class CodeAgent:
    """
    Specialized agent responsible for handling code-related requests.
    """

    def __init__(self, llm):
        self.llm = llm

    async def execute(self, task: str) -> CodeResult:
        """
        Generate a clear and practical coding response for the user's task.
        """
        structured_llm = self.llm.with_structured_output(CodeResult)

        system_prompt = """
        You are the Code Agent in a modular agentic system.

        Your responsibility is to handle requests that require writing,
        explaining, debugging, or modifying code.

        RULES:
        - Focus only on the coding task provided by the user.
        - Produce practical and executable code whenever possible.
        - Keep the solution simple unless the task requires complexity.
        - Do not invent external dependencies unless they are necessary.
        - Clearly identify the programming language.
        - Provide a concise explanation of what the code does.
        - Do not perform business discovery.
        - Do not ask unrelated questions.
        - If important information is missing, make a reasonable minimal
          assumption and state it in the explanation.
        """

        messages = [
            ("system", system_prompt),
            ("human", task),
        ]

        return await structured_llm.ainvoke(messages)