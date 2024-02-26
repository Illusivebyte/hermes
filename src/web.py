from flask import Flask, request, abort
from logging import getLogger
from queue import Queue

_SECRETS = list()
_MESSAGES: Queue = None
_LOGGER = getLogger("mattermost-hook-helper.web")

def set_secrets(secrets):
    global _SECRETS
    _SECRETS = secrets

def set_messages(messages):
    global _MESSAGES
    _MESSAGES = messages

app = Flask("mattermost hook helper")

def run():
    global app
    app.run(host="0.0.0.0")

@app.route("/hooks/<id>", methods=["POST"])
def hook(id: str) -> str:
    if id not in _SECRETS:
        _LOGGER.error("bad hook id")
        abort(404)
    _LOGGER.info(f"received request for id: {id}")
    _LOGGER.info(f"contents:{request.get_json()}")
    _MESSAGES.put(request.json)
    return "<p>Ok</p>"
