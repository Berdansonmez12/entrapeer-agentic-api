from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import get_settings


class LLMService:
    """
    Centralized service responsible for creating and providing
    the language model used by the agent system.
    """

    def __init__(
        self,
        model: str = "gemini-3.6-flash",
        temperature: float = 0,
    ):
        settings = get_settings()

        self.model = ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            google_api_key=settings.google_api_key,
        )

    def get_model(self) -> ChatGoogleGenerativeAI:
        return self.model