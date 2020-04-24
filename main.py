from flask import (
    Flask,
    jsonify,
    request
)
from flask_cors import CORS
import logging
import signal
import uuid
from telestrations import (
    Player,
    GameState
)

ADMIN_UID = None

logging.basicConfig(
    format="[%(asctime)s] - %(levelname)s/%(name)s: %(message)s",
    level=logging.DEBUG
)
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

app = Flask("telestrations", static_url_path=".")
CORS(app)

# TODO: define decorator function for doing admin authentication


# General use
@app.route("/game-state")
def game_state():
    ret = {"state": str(GameState.UNKNOWN), "message": None}
    return jsonify(ret)


# Game administration endpoints
@app.route("/game")
def game_admin_page():
    return "<h1>Admin Page</h1>"


@app.route("/game/authenticate", methods=["put"])
def game_admin_auth():
    return 400


@app.route("/game/start", methods=["put"])
def game_admin_start():
    return 400


@app.route("/game/next-round", methods=["put"])
def game_admin_next_round():
    return 400


@app.route("/game/current-round/time-remaining")
def game_time_remaining():
    return 400


# Player portal endpoints
@app.route("/")
def player_page():
    return "<h1>Player page</h1>"


@app.route("/player/add", methods=["post"])
def player_add():
    ret = {"name": "test", "id": None}
    return jsonify(ret)


@app.route("/player/:uid", methods=["post"])
def player_submit():
    return 400


def shutdown(*_):
    pass


if __name__ == "__main__":
    ADMIN_UID = uuid.uuid4()
    try:
        app.run(host="127.0.0.1", debug=True)
    except KeyboardInterrupt:
        shutdown()