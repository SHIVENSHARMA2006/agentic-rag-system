from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a response from the LLM.
        """
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """
        Verify provider availability.
        """
        pass