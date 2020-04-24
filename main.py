from flask import (
    Flask,
    jsonify,
    request
)
from flask_cors import CORS
import logging
import signal

logging.basicConfig(
    format="[%(asctime)s] - %(levelname)s/%(name)s: %(message)s",
    level=logging.DEBUG
)
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

app = Flask("telestrations", static_url_path=".")
CORS(app)


def shutdown(*_):
    pass


if __name__ == "__main__":
    try:
        app.run(host="127.0.0.1", debug=True)
    except KeyboardInterrupt:
        shutdown()