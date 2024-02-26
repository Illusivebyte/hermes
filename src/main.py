import yaml
from pathlib import Path
from logging import getLogger, Formatter, DEBUG, StreamHandler
from queue import Queue
from threading import Thread
from typing import List
import web
import bot

_LOGGER = getLogger("mattermost-hook-helper")
formatter = Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s')
ch = StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(DEBUG)
_LOGGER.addHandler(ch)
_LOGGER.setLevel(DEBUG)            


def load_config() -> dict:
    config = Path("config.yml")
    if not config.exists():
        _LOGGER.error("config file does not exist")
        exit(1)
    if not config.is_file():
        _LOGGER.error("config file path is not a file")
        exit(1)
    with open(config, "r") as f:
        config_text = f.read()
    config_obj = yaml.load(config_text, yaml.SafeLoader)
    return config_obj
    

def load_secrets() -> List:
    secrets = Path("secrets.yml")
    if not secrets.exists():
        _LOGGER.error("secrets file does not exist")
        exit(1)
    if not secrets.is_file():
        _LOGGER.error("secrets file path is not a file")
        exit(1)
    with open(secrets, "r") as f:
        secrets_text = f.read()
    secrets_obj = yaml.load(secrets_text, yaml.SafeLoader)
    if "secrets" in secrets_obj and type(secrets_obj["secrets"]) == list:
        secrets_list = secrets_obj["secrets"]
    if len(secrets_list) == 0: 
        _LOGGER.error("no secrets detected")
        exit(1)
    return secrets_list


if __name__ == "__main__":
    s_list = load_secrets()
    c_obj = load_config()
    msgs = Queue()
    bot.set_config(c_obj)
    bot.set_messages(msgs)
    Thread(target=bot.run).start()
    web.set_secrets(s_list)
    web.set_messages(msgs)
    web.run()

    


