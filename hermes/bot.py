from os import getenv
from logging import getLogger
from queue import Queue, Empty
from mattermostdriver import Driver
from hermes.formatters.github import GithubFormatter

_CONFIG = None
_LOGGER = getLogger("hermes.bot")
_MESSAGES: Queue = None


def set_config(config):
    global _CONFIG
    _CONFIG = config


def set_messages(messages):
    global _MESSAGES
    _MESSAGES = messages


def run() -> None:
    global _MESSAGES
    driver = Driver({
        "url": _CONFIG["url"],
        "token": _CONFIG["token"],
        "port": _CONFIG["port"]
    })
    driver.login()
    channel_id = driver.channels.get_channel_by_name_and_team_name(_CONFIG["team"], _CONFIG["channel"])['id']
    while True:
        try:
            msg_obj = _MESSAGES.get(block=False) 
        except Empty:
            continue
        attachments = GithubFormatter.format(msg_obj)
        driver.posts.create_post(options={
            "channel_id": channel_id, 
            "message": "",
            "props": {
                "attachments": attachments
            }
        })
