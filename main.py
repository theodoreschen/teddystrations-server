from flask import (
    Flask,
    jsonify,
    request
)
from flask_cors import CORS
from functools import wraps
import logging
import signal
import uuid
from teddystrations import (
    Player,
    GameState,
    RedisStateTracker
)
import sys

ADMIN_UID = None
STATE_TRACKER = None

logging.basicConfig(
    format="[%(asctime)s] - %(levelname)s/%(name)s: %(message)s",
    level=logging.DEBUG
)
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

app = Flask("teddystrations", static_url_path="")
CORS(app)


def admin_uid_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if (ADMIN_UID is not None) and\
            (request.args["uid"] != str(ADMIN_UID)):
            return "Invalid administrator UUID", 400
        return func(*args, **kwargs)
    return wrapper


# General use
@app.route("/game-state")
def game_state():
    state = STATE_TRACKER.get_state()
    if state == GameState.ROUND_ACTIVE or state == GameState.ROUND_IDLE:
        message = STATE_TRACKER.get_current_game_round()
    elif state == GameState.VIEWING_ACTIVE or state == GameState.VIEWING_IDLE:
        uid, message = STATE_TRACKER.get_viewing_uuid().values()
    return jsonify({"state": str(state), "message": message})


# Game administration endpoints
@app.route("/game", methods=["get", "delete"])
@admin_uid_check
def game_admin_page():
    return "<h1>Admin Page</h1>"


@app.route("/game/authenticate", methods=["put"])
@admin_uid_check
def game_admin_auth():
    return 400


@app.route("/game/start", methods=["put"])
@admin_uid_check
def game_admin_start():
    return 400


@app.route("/game/next-round", methods=["put"])
@admin_uid_check
def game_admin_next_round():
    return 400


@app.route("/game/current-round/time-remaining")
@admin_uid_check
def game_time_remaining():
    return 400


@app.route("/game/show-board", methods=["post"])
@admin_uid_check
def game_show_board():
    return 400


# Player portal endpoints
@app.route("/")
def player_page():
    if STATE_TRACKER.get_state() == GameState.UNAUTHENTICATED:
        return 404
    return "<h1>Player page</h1>"


@app.route("/player/add", methods=["post"])
def player_add():
    if STATE_TRACKER.get_state() != GameState.READY:
        return 404
    ret = {"name": "test", "id": None}
    return jsonify(ret)


@app.route("/player/:uid", methods=["post", "put"])
def player_submit():
    return 400


def init():
    global ADMIN_UID, STATE_TRACKER
    ADMIN_UID = uuid.uuid4()
    STATE_TRACKER = RedisStateTracker()
    STATE_TRACKER.set_admin_uuid(ADMIN_UID)
    STATE_TRACKER.set_state(GameState.UNAUTHENTICATED)


def shutdown(*_):
    global STATE_TRACKER
    STATE_TRACKER.close()


if __name__ == "__main__":
    init()

    sys.stderr.write(f"ADMIN UID: {ADMIN_UID}\n")
    sys.stderr.flush()
    try:
        app.run(host="127.0.0.1", debug=True)
    except KeyboardInterrupt:
        shutdown()