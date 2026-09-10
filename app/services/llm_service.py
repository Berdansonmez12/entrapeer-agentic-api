from langchain_openai import ChatOpenAI


class LLMService:
    """
    Centralized service responsible for creating and providing
    the language model used by the agent system.
    """

    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0):
        self.model = ChatOpenAI(
            model=model,
            temperature=temperature,
        )

    def get_model(self) -> ChatOpenAI:
        return self.model