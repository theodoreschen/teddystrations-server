from abc import (
    ABC,
    abstractmethod
)
from .data_types import GameState
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
    def set_state(self, state: GameState) -> bool:
        return True

    @abstractmethod
    def get_state(self) -> GameState:
        return GameState.UNKNOWN

    @abstractmethod
    def timer_start(self, duration: int=60):
        return

    @abstractmethod
    def timer_stop(self):
        return

    @abstractmethod
    def timer_time_remaining(self) -> int:
        return -1

