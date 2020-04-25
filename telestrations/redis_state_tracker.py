import redis
from .state_tracker import AbstractStateTracker
import uuid
from .data_types import GameState


class RedisStateTracker(AbstractStateTracker):
    _client: redis.Redis = None

    def __init__(self, *, host="localhost", port="6379"):
        self._client = redis.Redis(
            host="localhost", port="6379", 
            connection_pool=redis.BlockingConnectionPool()
        )

    def set_admin_uuid(self, uid: uuid.UUID):
        self._client.hset("admin", "uuid", str(uid))
        return
    set_admin_uuid.__doc__ = AbstractStateTracker.set_admin_uuid.__doc__

    def get_admin_uuid(self) -> uuid.UUID:
        uid = self._client.hget("admin", "uuid").decode('utf8')
        return uuid.UUID(uid)
    get_admin_uuid.__doc__ = AbstractStateTracker.get_admin_uuid.__doc__

    def set_number_of_game_rounds(self, rounds: int):
        return super().set_number_of_game_rounds()

    def get_number_of_game_rounds(self) -> int:
        return super().get_number_of_game_rounds()

    def set_current_game_round(self, round: int):
        return super().set_current_game_round()

    def get_current_game_round(self) -> int:
        return super().get_current_game_round()

    def set_viewing_uuid(self, uid: uuid.UUID, round: int=0):
        return super().set_viewing_uuid()
    
    def get_viewing_uuid(self) -> int:
        return super().get_viewing_uuid()

    def set_state(self, state: GameState):
        return super().set_state(state)

    def get_state(self) -> GameState:
        return super().get_state()

    def timer_start(self, duration: int=60):
        return super().timer_start(duration=duration)

    def timer_stop(self):
        return super().timer_stop()

    def timer_time_remaining(self) -> int:
        return super().timer_time_remaining()