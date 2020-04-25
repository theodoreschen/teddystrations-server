from abc import (
    ABC,
    abstractmethod
)
from .data_types import GameState
from uuid import UUID


class AbstractStateTracker(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def set_admin_uuid(self, uid: UUID):
        """
        :param a_uuid UUID: Administrative UUID value
        """
        return

    @abstractmethod
    def get_admin_uuid(self) -> UUID:
        return None

    @abstractmethod
    def set_number_of_game_rounds(self, rounds: int):
        return

    @abstractmethod
    def get_number_of_game_rounds(self) -> int:
        return -1

    @abstractmethod
    def set_current_game_round(self, round: int):
        return

    @abstractmethod
    def get_current_game_round(self) -> int:
        return -1

    @abstractmethod
    def set_viewing_uuid(self, uid: UUID, round: int=0):
        return

    @abstractmethod
    def get_viewing_uuid(self) -> UUID:
        return None

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

