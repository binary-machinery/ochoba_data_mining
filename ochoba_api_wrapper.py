import requests


class OchobaApiWrapper:
    def __init__(self, config):
        self.url = config["url"]
        self.headers = {"X-Device-Token": config["token"]}

    def execute(self, endpoint):
        return requests.get(self.url + endpoint, headers=self.headers)
