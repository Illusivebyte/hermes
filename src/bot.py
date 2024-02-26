from logging import getLogger
from queue import Queue, Empty
from mattermostdriver import Driver

_CONFIG = None
_LOGGER = getLogger("mattermost-hook-helper.bot")
_MESSAGES: Queue = None


def set_config(config):
    global _CONFIG
    _CONFIG = config


def set_messages(messages):
    global _MESSAGES
    _MESSAGES = messages


def prettify(json_obj) -> str:
    message = ""
    for key in json_obj:
        message += f"### {key}\n"
        if type(json_obj[key]) is list:
            for item in json_obj[key]:
                message += f"- {item}\n"
        elif type(json_obj[key]) is dict:
            for sub_key in json_obj[key]:
                message += f"#### {sub_key}\n{json_obj[key][sub_key]}\n"
        else:
            message += f"{key}\n"
    return message


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
            item = _MESSAGES.get(block=False) 
        except Empty:
            continue
        item = prettify(item)
        _LOGGER.info(f"sending message: {item}")
        driver.posts.create_post(options={
            'channel_id': channel_id, 
            'message': str(item)
            })
