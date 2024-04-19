from hermes.formatters.formatter import Formatter
from typing import Dict, List, Tuple

@Formatter.register
class GithubFormatter(Formatter):
    @staticmethod
    def get_name() -> str:
        return "github"

    @staticmethod
    def format(msg_obj: Dict) -> List:
        if "X-GitHub-Event" not in msg_obj["headers"]:
            return [{}]
        headers = msg_obj["headers"]
        event = headers.get("X-GitHub-Event")
        json_obj = msg_obj["payload"]
        attachment = GithubFormatter._baseline(event)
        attachment = GithubFormatter._repository(json_obj, attachment)
        attachment = GithubFormatter._organization(json_obj, attachment)
        attachment = GithubFormatter._sender(json_obj, attachment)

        match event:
            case "ping":
                attachment = GithubFormatter._ping(json_obj, attachment)
            case "push":
                attachment = GithubFormatter._push(json_obj, attachment)
        return [attachment]


    @staticmethod
    def _baseline(event: str) -> Dict:
        attachment = dict()
        attachment["author_name"] = "GitHub"
        attachment["author_icon"] = "https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png"
        attachment["author_link"] = "https://github.com"
        attachment["thumb_url"] = "https://github.githubassets.com/assets/GitHub-Logo-ee398b662d42.png"
        tokens = event.split()
        tokens = [token[0].upper() + token[1:] for token in tokens]
        event_name = " ".join(tokens)
        attachment["title"] = event_name
        return attachment
    

    @staticmethod
    def _repository(json_obj: Dict, attachment: Dict) -> Dict:
        if "repository" in json_obj:
            repository = json_obj["repository"]
            repo_name = repository["full_name"]
            repo_url = repository["html_url"]
            if "text" not in attachment:
                attachment["text"] = ""
            attachment["text"] = f"organization: [{repo_name}]({repo_url})"
        return attachment


    @staticmethod
    def _organization(json_obj: Dict, attachment: Dict) -> Dict:
        if "organization" in json_obj:
            organization = json_obj["organization"]
            org_name = organization["login"]
            org_url = organization["url"]
            if "text" not in attachment:
                attachment["text"] = ""
            attachment["text"] = f"organization: [{org_name}]({org_url})"
        return attachment

    
    @staticmethod
    def _sender(json_obj: Dict, attachment: Dict) -> Dict:
        if "sender" in json_obj:
            sender = json_obj["sender"]
            sender_name = sender["login"]
            sender_icon = sender["avatar_url"] 
            attachment["footer"] = f"sender: {sender_name}"
            attachment["footer_icon"] = sender_icon
        return attachment

# EVENT FUNCTIONS

    @staticmethod
    def _ping(json_obj: Dict, attachment: Dict) -> Dict:
        attachment["color"] = "#5F00FF"  # purple
        zen = json_obj["zen"]
        attachment["fields"] = [
            {"short": True, "title": "Zen", "value": zen}
        ]
        return attachment
    
    @staticmethod 
    def _push(json_obj: Dict, attachment: Dict) -> Dict:
        fields = list()
        if json_obj["deleted"]:
            attachment["color"] = "#000000"  # black
            fields.append({"short": True, "title": "Push Type", "value": "delete"})
        elif json_obj["created"]:
            attachment["color"] = "#00FF20" # green
            fields.append({"short": True, "title": "Push Type", "value": "create"})
        elif json_obj["forced"]:
            attachment = "#D000FF" # magenta
            fields.append({"short": True, "title": "Push Type", "value": "forced"})
        commits = json_obj["commits"]
        
        commits_str = ""
        for commit in commits:
            if len(commits_str) != 0:
                commits_str += "\n"
            commit_id = commit["id"]
            commit_url = commit["url"]
            commit_message = commit["message"]
            commits_str += f"[{commit_id}]({commit_url}): {commit_message}"
        fields.append({"short": False, "title": "Commits", "value": commits_str})
        attachment["fields"] = fields
        return attachment
