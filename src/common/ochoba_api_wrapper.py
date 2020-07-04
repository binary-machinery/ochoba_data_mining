from requests_toolbelt import sessions

class OchobaApiWrapper:
    def __init__(self, config):
        self.url = config["url"]
        self.session = sessions.BaseUrlSession(base_url=self.url)
        self.session.headers.update({"X-Device-Token": config["token"]})

    def execute(self, endpoint):
        return self.session.get(endpoint)
