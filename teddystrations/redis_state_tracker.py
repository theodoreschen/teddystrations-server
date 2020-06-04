import redis
from .state_tracker import AbstractStateTracker
import uuid
from .data_types import GameState, Player, Timer, str_to_game_state
import time


class RedisStateTracker(AbstractStateTracker):
    _client: redis.Redis = None

    def __init__(self, *, host: str = "localhost", port=6379):
        self._client = redis.Redis(
            host=host,
            port=port,
            # connection_pool=redis.BlockingConnectionPool()
        )

    def close(self):
        self._client.close()

    def set_admin_uuid(self, uid: uuid.UUID):
        self._client.hset("admin", "uuid", str(uid))
        return

    set_admin_uuid.__doc__ = AbstractStateTracker.set_admin_uuid.__doc__

    def get_admin_uuid(self) -> uuid.UUID:
        uid = self._client.hget("admin", "uuid").decode("utf8")
        return uuid.UUID(uid)

    get_admin_uuid.__doc__ = AbstractStateTracker.get_admin_uuid.__doc__

    def set_number_of_game_rounds(self, rounds: int):
        pipe = self._client.pipeline()
        pipe.hset("game", "rounds", str(rounds))
        pipe.set("current-round", "1")
        pipe.execute()
        return

    set_number_of_game_rounds.__doc__ = (
        AbstractStateTracker.set_number_of_game_rounds.__doc__
    )

    def get_number_of_game_rounds(self) -> int:
        rounds = int(self._client.hget("game", "rounds").decode("utf8"))
        return rounds

    get_number_of_game_rounds.__doc__ = (
        AbstractStateTracker.get_number_of_game_rounds.__doc__
    )

    def set_current_game_round(self, round: int):
        self._client.set("current-round", str(round))
        return

    set_current_game_round.__doc__ = AbstractStateTracker.set_current_game_round.__doc__

    def increment_game_round(self):
        self._client.incr("current-round")

    increment_game_round.__doc__ = AbstractStateTracker.increment_game_round.__doc__

    def decrement_game_round(self):
        self._client.decr("current-round")

    decrement_game_round.__doc__ = AbstractStateTracker.decrement_game_round.__doc__

    def get_current_game_round(self) -> int:
        try:
            r = self._client.get("current-round").decode()
        except Exception as e:
            return -1
        return int(r)

    def set_viewing_uuid(self, uid: uuid.UUID, index: int = 0):
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

    def timer_start(self, duration: int = 60):
        current_time = int(time.time())
        self._client.hmset(
            "timer", {"timer-start": str(current_time), "duration": str(duration)}
        )
        return

    timer_start.__doc__ = AbstractStateTracker.timer_start.__doc__

    def timer_stop(self):
        t = self._client.hgetall("timer")
        new_start_time = int(t[b"timer-start"]) + int(t[b"duration"])
        self._client.hmset(
            "timer", {"timer-start": str(new_start_time), "duration": "0"}
        )
        return

    timer_stop.__doc__ = AbstractStateTracker.timer_stop.__doc__

    def get_timer_info(self) -> Timer:
        t = self._client.hgetall("timer")
        # t = {k.decode(): v.decode() for k, v in timer_info.items()}
        timer = Timer(timer_start=int(t[b"timer-start"]), duration=int(t[b"duration"]))
        return timer

    get_timer_info.__doc__ = AbstractStateTracker.get_timer_info.__doc__

    def add_player(self, name: str, uid: uuid.UUID):
        pipe = self._client.pipeline()
        pipe.sadd("players", str(uid))
        pipe.rpush("player-order", str(uid))
        pipe.hset(str(uid), "name", name)
        pipe.execute()
        return

    add_player.__doc__ = AbstractStateTracker.add_player.__doc__

    def get_player(self, uid: uuid.UUID) -> dict:
        return super().get_player(uid)

    def get_num_of_players(self) -> int:
        players_uids = self._client.smembers("players")
        num_players = self._client.llen("player-order")
        if len(players_uids) != num_players:
            print(
                "Game state inconsistency - number of player UUIDs don't match number of tracked players"
            )
        return num_players

    get_num_of_players.__doc__ = AbstractStateTracker.get_num_of_players.__doc__

    def get_all_players(self) -> list:
        player_uids = [uid.decode() for uid in self._client.smembers("players")]
        players = []
        for uid in player_uids:
            player_name = self._client.hget(uid, "name")
            p = Player(name=player_name.decode(), uid=uid)
            players.append(p.to_dict())
        return players

    get_all_players.__doc__ = AbstractStateTracker.get_all_players.__doc__

    def get_player_order(self) -> list:
        num_players = self._client.llen("player-order")
        players = self._client.lrange("player-order", 0, num_players)
        players = [p.decode("utf8") for p in players]
        return players

    get_player_order.__doc__ = AbstractStateTracker.get_player_order.__doc__

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
        pipe.delete("current-round-submissions")
        pipe.delete("player-order")
        pipe.execute()
        return

    reset_game_state.__doc__ = AbstractStateTracker.reset_game_state.__doc__

    def round_submission_add_player(self, uid: uuid.UUID):
        self._client.rpush("current-round-submissions", str(uid))
        return

    round_submission_add_player.__doc__ = (
        AbstractStateTracker.round_submission_add_player.__doc__
    )

    _CACHED_NUM_OF_SUBMISSIONS: int = 0
    _CACHED_PLAYERS_WHO_SUBMITTED = []

    def round_submission_all_players(self) -> list:
        num_submissions = self._client.llen("current-round-submissions")
        if num_submissions == self._CACHED_NUM_OF_SUBMISSIONS:
            return self._CACHED_PLAYERS_WHO_SUBMITTED

        # we can't assume the cached results are the same across multiple UWSGI threads
        self._CACHED_NUM_OF_SUBMISSIONS = num_submissions
        self._CACHED_PLAYERS_WHO_SUBMITTED = []

        player_uids = self._client.lrange(
            "current-round-submissions", 0, num_submissions
        )
        player_uids = [p.decode("utf8") for p in player_uids]
        for uid in player_uids:
            player_name = self._client.hget(uid, "name")
            p = Player(name=player_name.decode(), uid=uuid.UUID(uid))
            self._CACHED_PLAYERS_WHO_SUBMITTED.append(p.to_dict())

        return self._CACHED_PLAYERS_WHO_SUBMITTED

    round_submission_all_players.__doc__ = (
        AbstractStateTracker.round_submission_all_players.__doc__
    )

    def round_submission_clear(self):
        self._CACHED_NUM_OF_SUBMISSIONS = 0
        self._CACHED_PLAYERS_WHO_SUBMITTED = []
        self._client.delete("current-round-submissions")
        return

    round_submission_clear.__doc__ = AbstractStateTracker.round_submission_clear.__doc__
