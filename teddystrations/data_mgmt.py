from abc import (
    ABC,
    abstractmethod
)
from uuid import UUID
from .data_types import Player


class AbstractDataMgmt(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def add_player(self, name) -> Player:
        return None

    @abstractmethod
    def get_player(self, uid: str) -> Player:
        return None

    @abstractmethod
    def delete_player(self, uid: str) -> Player:
        return None

    @abstractmethod
    def add_content(self, uid: str, content: str):
        return

    @abstractmethod
    def retrieve_content(self, uid: str):
        return
