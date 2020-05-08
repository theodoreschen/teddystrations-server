from abc import (
    ABC,
    abstractmethod
)
from uuid import UUID
from .data_types import Player


class AbstractDataMgmt(ABC):
    _game_uuid = None

    def __init__(self, game_uuid: UUID):
        self._game_uuid = str(game_uuid)

    @abstractmethod
    def close(self):
        return

    @abstractmethod
    def set_game_details(self, rounds: int):
        return

    @abstractmethod
    def delete_game(self):
        return

    @abstractmethod
    def reset_game(self):
        return

    @abstractmethod
    def add_player(self, name: str, player_uuid: UUID):
        return

    @abstractmethod
    def get_player(self, uid: UUID) -> Player:
        return None

    @abstractmethod
    def delete_player(self, uid: UUID) -> Player:
        return None

    @abstractmethod
    def add_content(self, uid: UUID, content: str, game_round: int):
        return

    @abstractmethod
    def retrieve_content(self, uid: UUID):
        return
