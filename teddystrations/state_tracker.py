from abc import ABC, abstractmethod
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
        """
        Sets the number of rounds as well as initializes current round to 1

        :param rounds int: Number of rounds in the game
        """
        return

    @abstractmethod
    def get_number_of_game_rounds(self) -> int:
        """
        :return: number of rounds
        :rtype: int
        """
        return -1

    @abstractmethod
    def set_current_game_round(self, round: int):
        """
        Sets the current round to input

        :param round int: current round to force the game to
        """
        return

    @abstractmethod
    def increment_game_round(self):
        """
        Increments the current round value by 1
        """
        return

    @abstractmethod
    def decrement_game_round(self):
        """
        Decrements the current round value by 1
        """
        return

    @abstractmethod
    def get_current_game_round(self) -> int:
        """
        :return: current round value
        :rtype: int
        """
        return -1

    @abstractmethod
    def set_viewing_uuid(self, uid: UUID, index: int = 0):
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
    def timer_start(self, duration: int = 60):
        """
        :param duration int: number of seconds to set the timer
        """
        return

    @abstractmethod
    def timer_stop(self):
        """
        Ends timer
        """
        return

    @abstractmethod
    def get_timer_info(self) -> dict:
        """
        :return: information about timer
        :rtype: dict
        """
        return {}

    @abstractmethod
    def add_player(self, name: str, uid: UUID):
        """
        :param name str: Name of player
        :param uuid UUID: Generated UUID for player
        """
        return

    @abstractmethod
    def get_player(self, uid: UUID) -> dict:
        return {}

    @abstractmethod
    def get_num_of_players(self) -> int:
        """
        :return: number of players registered
        :rtype: int
        """
        return -1

    @abstractmethod
    def get_all_players(self) -> list:
        """
        :return: A list of all Player objects registered
        :rtype: list
        """
        return []

    @abstractmethod
    def get_player_order(self) -> list:
        """
        :return: A list of all Player UUIDs
        :rtype: list
        """
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

    @abstractmethod
    def round_submission_add_player(self, uid: UUID):
        """
        Add player who's submitted to the current round

        :param uid UUID: player UUID
        """
        return

    @abstractmethod
    def round_submission_all_players(self) -> list:
        """
        Fetch all players who have completed their submission for the round

        :return: a list of all Players
        :rtype: list
        """
        return []

    @abstractmethod
    def round_submission_clear(self):
        """
        Clear submission list
        """
        return
