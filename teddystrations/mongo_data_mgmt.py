from .data_mgmt import AbstractDataMgmt
from uuid import UUID
from .data_types import Player


class MongoDataMgmt(AbstractDataMgmt):
    def __init__(self):
        pass

    def add_player(self, name: str) -> Player:
        return super().add_player(name)

    def get_player(self, uid: UUID) -> Player:
        return super().get_player(uid)

    def delete_player(self, uid) -> Player:
        return super().delete_player(uid)

    def add_content(self, uid: UUID, content: str):
        return super().add_content(uid, content)

    def retrieve_content(self, uid: UUID):
        return super().retrieve_content(uid)
