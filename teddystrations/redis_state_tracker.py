import redis
from .state_tracker import AbstractStateTracker
import uuid
from .data_types import (
    GameState,
    Player,
    str_to_game_state
)
import time


class RedisStateTracker(AbstractStateTracker):
    _client: redis.Redis = None

    def __init__(self, *, host="localhost", port="6379"):
        self._client = redis.Redis(
            host="localhost", port="6379", 
            connection_pool=redis.BlockingConnectionPool()
        )

    def close(self):
        self._client.close()

    def set_admin_uuid(self, uid: uuid.UUID):
        self._client.hset("admin", "uuid", str(uid))
        return
    set_admin_uuid.__doc__ = AbstractStateTracker.set_admin_uuid.__doc__

    def get_admin_uuid(self) -> uuid.UUID:
        uid = self._client.hget("admin", "uuid").decode('utf8')
        return uuid.UUID(uid)
    get_admin_uuid.__doc__ = AbstractStateTracker.get_admin_uuid.__doc__

    def set_number_of_game_rounds(self, rounds: int):
        pipe = self._client.pipeline()
        pipe.hset("game", "rounds", str(rounds))
        pipe.set("current-round", "1")
        pipe.execute()
        return

    def get_number_of_game_rounds(self) -> int:
        rounds = int(self._client.hget("game", "rounds").decode('utf8'))
        return rounds

    def set_current_game_round(self, round: int):
        self._client.set("current-round", str(round))
        return

    def increment_game_round(self):
        self._client.incr("current-round")

    def decrement_game_round(self):
        self._client.decr("current-round")

    def get_current_game_round(self) -> int:
        return super().get_current_game_round()

    def set_viewing_uuid(self, uid: uuid.UUID, index: int=0):
        return super().set_viewing_uuid()
    
    def get_viewing_uuid(self) -> dict:
        return super().get_viewing_uuid()

    def set_state(self, state: GameState):
        self._client.hset("game", "state", str(state))
        return
    set_state.__doc__ = AbstractStateTracker.set_state.__doc__

    def get_state(self) -> GameState:
        state = self._client.hget("game", "state").decode("utf8")
        return str_to_game_state(state)
    get_state.__doc__ = AbstractStateTracker.set_state.__doc__

    def timer_start(self, duration: int=60):
        current_time = int(time.time())
        self._client.hmset(
            "timer", 
            {"timer-start": str(current_time), "duration": str(duration)}
        )
        return 

    def timer_stop(self):
        # self._client.hgetall("timer").decode()
        return super().timer_stop()

    def timer_time_remaining(self) -> int:
        return super().timer_time_remaining()
    
    def add_player(self, name: str, uid: uuid.UUID):
        pipe = self._client.pipeline()
        pipe.sadd("players", str(uid))
        pipe.hset(str(uid), "name", name)
        pipe.execute()
        return

    def get_player(self, uid: uuid.UUID) -> dict:
        return super().get_player(uid)

    def get_num_of_players(self) -> int:
        players_uids = self._client.smembers("players")
        return len(players_uids)

    def get_all_players(self) -> list:
        player_uids = [uid.decode() for uid in self._client.smembers("players")]
        players = []
        for uid in player_uids:
            player_name = self._client.hget(uid, "name")
            p = Player(name=player_name.decode(), uid=uid)
            players.append(p.to_dict())
        return players

    def delete_player(self, uid: uuid.UUID):
        return super().delete_player(uid)

    def reset_game_state(self):
        player_uids = [uid.decode() for uid in self._client.smembers("players")]
        pipe = self._client.pipeline()

        # self.set_state(GameState.UNAUTHENTICATED)
        pipe.hset("game", "state", str(GameState.UNAUTHENTICATED))
        pipe.hdel("game", "rounds")
        for uid in player_uids:
            pipe.delete(uid)
        pipe.delete("players")
        pipe.delete("current-round")
        pipe.execute()
        return