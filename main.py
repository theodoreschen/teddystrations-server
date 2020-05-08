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
    RedisStateTracker,
    MongoDataMgmt
)
import sys
import argparse

DEBUG = True
ADMIN_UID = None
STATE_TRACKER = None
DB = None

ROUND_DURATION = 120 #seconds

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
        if ADMIN_UID is None:
            return "Unhandled server error state", 500
        if request.args["uid"] != str(ADMIN_UID):
            return "Invalid administrator UUID", 400
        return func(*args, **kwargs)
    return wrapper


# General use
@app.route("/game-state")
def game_state():
    state = STATE_TRACKER.get_state()
    message = None
    if state == GameState.ROUND_ACTIVE or state == GameState.ROUND_IDLE:
        message = STATE_TRACKER.get_current_game_round()
    elif state == GameState.VIEWING_ACTIVE or state == GameState.VIEWING_IDLE:
        uid, message = STATE_TRACKER.get_viewing_uuid().values()
    return jsonify({"state": str(state), "message": message})


# Game administration endpoints
@app.route("/game", methods=["get", "delete"])
def game_admin():
    """
    GET/DELETE /game?uid=UUID
    """
    @admin_uid_check
    def reset_game():
        STATE_TRACKER.reset_game_state()
        return '', 200

    if request.method == "DELETE":
        return reset_game()
    elif request.method == "GET":
        return "<h1>Admin Page</h1>"
    return '', 404


@app.route("/game/authenticate", methods=["put"])
@admin_uid_check
def game_admin_auth():
    STATE_TRACKER.set_state(GameState.READY)
    return '', 200


@app.route("/game/players", methods=["get"])
@admin_uid_check
def game_admin_players():
    """
    GET /game/players?uid=UUID
    """
    players = STATE_TRACKER.get_all_players()
    return jsonify(players), 200


@app.route("/game/start", methods=["put"])
@admin_uid_check
def game_admin_start():
    """
    PUT /game/start?uid=UUID&nplayers=INT
    """
    # calculate and set number of rounds
    num_of_players = STATE_TRACKER.get_num_of_players()
    STATE_TRACKER.set_number_of_game_rounds(num_of_players)
    # update state
    STATE_TRACKER.set_state(GameState.ROUND_ACTIVE)
    STATE_TRACKER.set_current_game_round(1)
    # start timer
    STATE_TRACKER.timer_start(ROUND_DURATION)
    return '', 200


@app.route("/game/end-round", methods=["put"])
@admin_uid_check
def game_admin_end_round():
    STATE_TRACKER.timer_stop()
    STATE_TRACKER.set_state(GameState.ROUND_IDLE)
    return '', 200


@app.route("/game/next-round", methods=["put"])
@admin_uid_check
def game_admin_next_round():
    if STATE_TRACKER.get_number_of_game_rounds() == STATE_TRACKER.get_current_game_round():
        STATE_TRACKER.set_state(GameState.VIEWING_IDLE)
    else:
        STATE_TRACKER.set_state(GameState.ROUND_ACTIVE)
        STATE_TRACKER.increment_game_round()
        STATE_TRACKER.timer_start(ROUND_DURATION)
    return '', 200


@app.route("/game/current-round/time-remaining")
@admin_uid_check
def game_time_remaining():
    """
    GET /game/current-round/time-remaining?uid=UUID
    """
    t = STATE_TRACKER.get_timer_info()
    time_remaining = t.time_remaining()
    if time_remaining < 0:
        time_remaining = 0
    retobj = {
        "round": STATE_TRACKER.get_current_game_round(),
        "totalRounds": STATE_TRACKER.get_number_of_game_rounds(),
        "roundDuration": t.duration,
        "timeRemaining": time_remaining
    }
    return jsonify(retobj), 200


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
    data = request.get_json()
    # TODO: jsonschema check data
    player_uid = uuid.uuid4()
    STATE_TRACKER.add_player(data["name"], player_uid)
    return jsonify({"name": data["name"], "uid": str(player_uid)}), 200


@app.route("/player/:uid", methods=["post", "put"])
def player_submit():
    return 400


def init():
    global STATE_TRACKER, DB
       
    STATE_TRACKER = RedisStateTracker()
    STATE_TRACKER.set_admin_uuid(ADMIN_UID)
    STATE_TRACKER.set_state(GameState.UNAUTHENTICATED)

    DB = MongoDataMgmt(ADMIN_UID)


def shutdown(*_):
    global STATE_TRACKER
    STATE_TRACKER.close()
    DB.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Launch the Teddystrations backend server")
    parser.add_argument('--debug', action='store_true', help="debug mode")
    parser.add_argument('uuid', help="game_uuid")
    args = parser.parse_args()

    DEBUG = args.debug
    if DEBUG:
        ADMIN_UID = uuid.UUID("01234567-0123-4567-89ab-0123456789ab")
    else:
        ADMIN_UID = uuid.UUID(args.uuid)

    sys.stderr.write(f"ADMIN UID: {ADMIN_UID}\n")
    sys.stderr.flush()
    try:
        app.run(host="127.0.0.1", debug=DEBUG)
    except KeyboardInterrupt:
        shutdown()
