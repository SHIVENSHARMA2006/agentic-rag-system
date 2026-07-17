from abc import ABC, abstractmethod


class BaseEmbeddingProvider(ABC):

    @abstractmethod
    def generate_embedding(self, text: str):
        """
        Generate an embedding vector.
        """
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """
        Verify provider availability.
        """
        pass