from abc import (
    ABC,
    abstractmethod
)


class AbstractStateTracker(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def setState(self, state: str) -> bool:
        return True

    @abstractmethod
    def getState(self) -> str:
        return ''
