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


_game_state_list = [name.lower() for name, _ in GameState.__members__.items()]
_game_state_map = {name.lower(): state for name, state in GameState.__members__.items()}

def str_to_game_state(state: str="unknown") -> GameState:
    if state.lower() not in _game_state_list:
        return GameState.UNKNOWN
    return _game_state_map[state.lower()]


class Player:
    name: str
    uid: uuid.UUID

    def __init__(self, name: str):
        self.name = name
        self.uid = uuid.uuid4()

    def to_dict(self) -> dict:
        """
        :return: dictionary representation of the Player object
        :rtype: dict
        """
        return {
            "name": self.name,
            "uid": str(self.uid)
        }

    def to_json(self) -> str:
        """
        :return: JSON-compatible string representation of the Player object
        :rtype: str
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, **kwargs):
        """
        :param name str: Player.name variable
        :param uid str: Player.uid variable. Must be valid UUID
        :return: a Player object with the attributes defined in the arguments
        """
        cls.name = kwargs["name"]
        cls.uid = uuid.UUID(kwargs["uid"])
        return cls

    @classmethod
    def from_json(cls, json_obj: str):
        """
        :param json_obj str: valid JSON-represented string of a Player object
        :return: a Player object with the attributes defined by json_obj
        """
        obj = json.loads(json_obj)
        return cls.from_dict(name=obj["name"], uid=obj["uid"])
