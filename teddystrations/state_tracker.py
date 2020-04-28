from abc import (
    ABC,
    abstractmethod
)
from .data_types import GameState
from uuid import UUID


# replace all dict with simple class objects


class AbstractStateTracker(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def set_admin_uuid(self, uid: UUID):
        """
        :param uid UUID: Administrative UUID value
        """
        return

    @abstractmethod
    def get_admin_uuid(self) -> UUID:
        """
        :return: administrator UUID object
        :rtype: UUID
        """
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
    def set_viewing_uuid(self, uid: UUID, index: int=0):
        return

    @abstractmethod
    def get_viewing_uuid(self) -> dict:
        return {"uid": "", "message": ""}

    @abstractmethod
    def set_state(self, state: GameState):
        """
        :param state GameState: current game state
        """
        return

    @abstractmethod
    def get_state(self) -> GameState:
        """
        :return: GameState object representative of current game state
        :rtype: GameState
        """
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

    @abstractmethod
    def add_player(self, uid: UUID):
        return

    @abstractmethod
    def get_player(self, uid: UUID) -> dict:
        return {}

    @abstractmethod
    def get_all_players(self) -> list:
        return []

    @abstractmethod
    def delete_player(self, uid: UUID):
        return

    @abstractmethod
    def reset_game_state(self):
        """
        Resets the game to its original state
        """
        return
