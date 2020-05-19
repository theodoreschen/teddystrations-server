from .data_mgmt import AbstractDataMgmt
from uuid import UUID
from .data_types import Player
import pymongo
import time

class MongoDataMgmt(AbstractDataMgmt):
    _client = None
    _db = None
    _game_data = None
    _players_data = None

    def __init__(self, game_uuid: UUID):
        super().__init__(game_uuid)
        self._client = pymongo.MongoClient(host="localhost", port=27017)
        
        teddystrations = self._client["teddystrations"]
        registered_games_db = teddystrations["registered_games"]

        if not registered_games_db.find({"game_id": str(self._game_uuid)}):
            registered_games_db.insert_one({"game_id": str(self._game_uuid)})

        self._db = self._client[self._game_uuid]
        self._game_data = self._db["game_data"]
        self._players_data = self._db["players_data"]

    def close(self):
        self._client.close()

    def set_game_details(self, rounds: int):
        self._game_data.insert_one({
            "page": "game_metadata",
            "rounds": rounds,
            "date": time.time()
        })
        return

    def delete_game(self):
        return super().delete_game()

    def reset_game(self):
        collection_list = []
        for collection in self._db.list_collections():
            collection_list.append(collection["name"])
        for collection_name in collection_list:
            self._db.drop_collection(collection_name)
        return

    def add_player(self, name: str, player_uuid: UUID):
        self._players_data.insert_one({
            "player_id": str(player_uuid)
        })
        uid = self._db[str(player_uuid)]
        uid.insert_one({
            "name": name
        })
        return 

    def get_player(self, uid: UUID) -> Player:
        return super().get_player(uid)

    def delete_player(self, uid) -> Player:
        return super().delete_player(uid)

    def add_content(
        self, player_uuid: UUID, origin_player_uuid:
        UUID, content: str, game_round: int
    ):
        puid = self._db[str(origin_player_uuid)]
        puid.insert_one({
            "content": content, "round": game_round,
            "originPlayer": str(player_uuid)
        })
        return
    add_content.__doc__ = AbstractDataMgmt.add_content.__doc__

    def retrieve_content(self, origin_player_uuid: UUID, game_round: int) -> dict:
        puid = self._db[str(origin_player_uuid)]
        obj = puid.find_one({"round": game_round})
        if obj:
            obj.pop("_id")
            return obj
        return {}
    retrieve_content.__doc__ = AbstractDataMgmt.retrieve_content.__doc__
