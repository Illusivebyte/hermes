from time import sleep
from logging import getLogger
from queue import Queue, Empty
from mattermostdriver import Driver
from hermes.formatters.github import GithubFormatter
from typing import Dict


_LOGGER = getLogger("hermes.bot")


class MattermostBot:
    def __init__(self, bot_config: Dict, msg_q: Queue) -> None:
        scheme = ""
        if "https" not in bot_config:
            scheme = "https"
        if "https" in bot_config:
            scheme = "http" if  not bot_config["https"] else "https"
        self.driver = Driver({
            "url": bot_config["url"],
            "token": bot_config["token"],
            "port": bot_config["port"],
            "scheme": scheme
        })
        self.team = bot_config["team"]
        self.channel = bot_config["channel"]
        self.msg_q = msg_q
        self.running = False

    def shutdown(self) -> None:
        _LOGGER.info("shutting down mattermost bot")
        self.running = False

    def run(self) -> None:
        _LOGGER.info("running mattermost bot")
        self.driver.login()
        channel_id = self.driver.channels.get_channel_by_name_and_team_name(self.team, self.channel)['id']
        self.running = True
        while self.running:
            try:
                msg_obj = self.msg_q.get(block=False) 
            except Empty:
                sleep(1)
                continue
            attachments = GithubFormatter.format(msg_obj)
            self.driver.posts.create_post(options={
                "channel_id": channel_id, 
                "message": "",
                "props": {
                    "attachments": attachments
                }
            })
        _LOGGER.info("mattermost bot has shutdown")

def create_bot(bot_config: Dict, msg_q: Queue) -> MattermostBot:
    return MattermostBot(bot_config, msg_q)
