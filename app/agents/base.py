from abc import ABC, abstractmethod
from time import perf_counter

from app.agents.state import GraphState
from app.core.logging import logger


class BaseAgent(ABC):
    """
    Base class for every LangGraph agent.

    Provides:
    - Logging
    - Execution timing
    - Exception handling
    - Metadata tracking
    """

    def run(
        self,
        state: GraphState,
    ) -> GraphState:

        agent_name = self.__class__.__name__

        metadata = state.setdefault(
            "metadata",
            {},
        )

        metadata.setdefault(
            "warnings",
            [],
        )

        metadata.setdefault(
            "timings",
            {},
        )

        metadata.setdefault(
            "services",
            {},
        )

        logger.info(
            f"{agent_name} started."
        )

        start = perf_counter()

        try:

            state = self.execute(state)

        except Exception as e:

            logger.exception(
                f"{agent_name} failed: {e}"
            )

            metadata["warnings"].append(
                f"{agent_name}: {str(e)}"
            )

        elapsed = perf_counter() - start

        metadata["timings"][
            agent_name
        ] = round(
            elapsed,
            3,
        )

        logger.info(
            f"{agent_name} completed in "
            f"{elapsed:.3f}s"
        )

        return state

    @abstractmethod
    def execute(
        self,
        state: GraphState,
    ) -> GraphState:
        """
        Agent business logic.
        """
        pass