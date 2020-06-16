import json
import pathlib


class ConfigLoader:
    @staticmethod
    def load():
        script_path = pathlib.Path(__file__).parent.absolute()
        with open(str(script_path) + "/config.json") as json_file:
            return json.load(json_file)
