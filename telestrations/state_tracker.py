from abc import (
    ABC,
    abstractmethod
)
from .utils import GameState
from uuid import UUID


class AbstractStateTracker(ABC):
    _game_rounds: int
    _current_round: int
    _viewing_uuid: UUID
    _admin_uuid: UUID

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def setState(self, state: GameState) -> bool:
        return True

    @abstractmethod
    def getState(self) -> GameState:
        return GameState.UNKNOWN

    @abstractmethod
    def timerStart(self, duration: int=60):
        return

    @abstractmethod
    def timerStop(self):
        return

    @abstractmethod
    def timerTimeRemaining(self) -> int:
        return -1

