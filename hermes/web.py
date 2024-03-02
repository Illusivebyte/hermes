from flask import Flask, request, abort
from logging import getLogger
from queue import Queue

_SECRETS = list()
_MESSAGES: Queue = None
_LOGGER = getLogger("hermes.web")

def set_secrets(secrets):
    global _SECRETS
    _SECRETS = secrets

def set_messages(messages):
    global _MESSAGES
    _MESSAGES = messages

app = Flask("hermes")

def run():
    global app
    app.run(host="0.0.0.0")

@app.route("/hooks/<id>", methods=["POST"])
def hook(id: str) -> str:
    if id not in _SECRETS:
        _LOGGER.error("bad hook id")
        abort(404)
    _LOGGER.debug(f"received request for id: {id}")
    _LOGGER.debug(f"header: {request.headers}")
    _LOGGER.debug(f"payload:{request.get_json()}")
    msg_obj = {"headers": request.headers, "payload": request.get_json()}
    _MESSAGES.put(msg_obj)
    return "<p>Ok</p>"
