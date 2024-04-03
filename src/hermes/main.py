import yaml
from pathlib import Path
from logging import getLogger, Formatter, DEBUG, StreamHandler
from queue import Queue
from threading import Thread
from typing import Dict
import hermes.web as web
import hermes.bot as bot

_LOGGER = getLogger("hermes")
formatter = Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s')
ch = StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(DEBUG)
_LOGGER.addHandler(ch)
_LOGGER.setLevel(DEBUG)            


def load_config() -> Dict:
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
    

def load_hooks() -> Dict:
    hooks = Path("hooks.yml")
    if not hooks.exists():
        _LOGGER.error("hooks file does not exist")
        exit(1)
    if not hooks.is_file():
        _LOGGER.error("hooks file path is not a file")
        exit(1)
    with open(hooks, "r") as f:
        hooks_text = f.read()
    hooks_obj = yaml.load(hooks_text, yaml.SafeLoader)
    if "hooks" in hooks_obj and type(hooks_obj["hooks"]) == list:
        hooks_list = hooks_obj["hooks"]
    if len(hooks_list) == 0: 
        _LOGGER.error("no hooks detected")
        exit(1)
    return hooks_obj


def main() -> None:
    hooks_d = load_hooks()
    config_o = load_config()
    msgs = Queue()
    bot_o = bot.create_bot(config_o, msgs)
    thread_o = Thread(target=bot_o.run)
    thread_o.start()
    app_o = web.HermesWeb(hooks_d, msgs)
    try:
        app_o.run()
    except KeyboardInterrupt:
        _LOGGER.info("shutting down")
    bot_o.shutdown()
    thread_o.join()
    _LOGGER.info("good bye")
    exit(0)


if __name__ == "__main__":
    main()
 