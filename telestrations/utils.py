from enum import Enum, auto
_game_state_list = [name.lower() for name, _ in GameState.__members__.items()]
_game_state_map = {name.lower(): state for name, state in GameState.__members__.items()}


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

    @classmethod
    def getGameState(cls, state: str="unknown") -> GameState:
        if state.lower() not in _game_state_list:
            return GameState.UNKNOWN
        return GameState[state]