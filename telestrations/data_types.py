import uuid
import json
from enum import Enum, auto


class GameState(Enum):
    UNKNOWN = auto()
    UNAUTHENTICATED = auto()
    READY = auto()
    STARTED = auto()
    ROUND_IDLE = auto()
    ROUND_ACTIVE = auto()
    FINISHED = auto()
    VIEWING_IDLE = auto()
    VIEWING_ACTIVE = auto()
    END = auto()

    def __str__(self):
        return f"{self.name.lower()}"

    # @classmethod
    # def get_game_state(cls, state: str="unknown") -> GameState:
    #     if state.lower() not in cls._game_state_list:
    #         return GameState.UNKNOWN
    #     return GameState[state]


_game_state_list = [name.lower() for name, _ in GameState.__members__.items()]
_game_state_map = {name.lower(): state for name, state in GameState.__members__.items()}


class Player:
    name: str
    uid: uuid.UUID

    def __init__(self, name: str):
        self.name = name
        self.uid = uuid.uuid4()

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "uid": str(self.uid)
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, obj: dict):
        cls.name = obj["name"]
        cls.uid = uuid.UUID(obj["uid"])
        return cls

    @classmethod
    def from_json(cls, json_obj: str):
        obj = json.loads(json_obj)
        return cls.from_dict(obj)
