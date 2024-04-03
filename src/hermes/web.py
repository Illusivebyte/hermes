from flask import Flask, request, abort
from logging import getLogger
from queue import Queue
from typing import Dict, Tuple
from waitress import serve


_LOGGER = getLogger("hermes.web")


class HermesWeb:
    def __init__(self, hooks_d: Dict, msg_q: Queue, host: str = "0.0.0.0", port: int = 8080) -> None:
        """
        A class containing the flask app and all required functions.

        :param hooks_d: the dictionary of hook id to hook secret
        :param msg_q: the message queue used to pass hooks to the mattermost bot
        :param host: the host address to serve from
        :param port: the host port to serve from
        """
        self.hooks_d = hooks_d
        self.msg_q = msg_q
        self.host = host
        self.port = port
        self.app = self.__create_app()

    def run(self) -> None:
        """
        Run hermes web app.
        """
        _LOGGER.info("serving hermes web app")
        serve(self.app, host=self.host, port=self.port)

    @staticmethod
    def search_for_hook(id: str, hooks_d: Dict) -> Tuple:
        for hook in hooks_d["hooks"]:
            if hook["id"] == id:
                return True, hook
        return False, dict()

    def __create_app(self) -> Flask:
        """
        Create a Flask app with all appropriate routes.

        :return: a Flask app
        """
        app = Flask("hermes")

        @app.route("/hooks/<id>", methods=["POST"])
        def hook(id: str) -> str:
            found, data = HermesWeb.search_for_hook(id, self.hooks_d)
            if not found:
                _LOGGER.error("bad hook id")
                abort(404)
            _LOGGER.debug(f"received request for id: {id}")
            _LOGGER.debug(f"header: {request.headers}")
            _LOGGER.debug(f"payload:{request.get_json()}")
            msg_obj = {"hook": data, "headers": request.headers, "payload": request.get_json()}
            self.msg_q.put(msg_obj)
            return "<p>Ok</p>"

        return app
