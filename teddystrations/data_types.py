import uuid
import json
from enum import Enum, auto
import time


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


def str_to_game_state(state: str = "unknown") -> GameState:
    if state.lower() not in _game_state_list:
        return GameState.UNKNOWN
    return _game_state_map[state.lower()]


class Player:
    name: str
    uid: uuid.UUID

    def __init__(self, *, name: str = None, uid: uuid.UUID = None):
        self.name = name
        self.uid = uid

        if self.uid is None:
            self.uid = uuid.uuid4()

        if self.name is None:
            self.name = str(self.uid)

    def to_dict(self) -> dict:
        """
        :return: dictionary representation of the Player object
        :rtype: dict
        """
        return {"name": self.name, "uid": str(self.uid)}

    def to_json(self) -> str:
        """
        :return: JSON-compatible string representation of the Player object
        :rtype: str
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_obj: str):
        """
        :param json_obj str: valid JSON-represented string of a Player object
        :return: a Player object with the attributes defined by json_obj
        """
        obj = json.loads(json_obj)
        return cls(name=obj["name"], uid=uuid.UUID(obj["uid"]))


class Timer:
    timer_start: int
    duration: int

    def __init__(self, *, timer_start: int = 0, duration: int = 0):
        self.timer_start = timer_start
        self.duration = duration

    def to_dict(self) -> dict:
        """
        :return: dict respresentation of the Timer object
        :rtype: dict
        """
        return {"timer_start": timer_start, "duration": duration}

    def time_remaining(self) -> int:
        """
        :return: time remaining on timer
        :rtype: int
        """
        current_time = int(time.time())
        return self.duration - (current_time - self.timer_start)

    def to_json(self) -> str:
        """
        :return: JSON-compatible string representation of the Timer object
        :rtype: str
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_obj: str):
        """
        :param json_obj str: valid JSON-represented string of a Timer object
        :return: a Player object with the attributes defined by json_obj
        """
        obj = json.loads(json_obj)
        return cls(timer_start=obj["timer_start"], duration=obj["duration"])
