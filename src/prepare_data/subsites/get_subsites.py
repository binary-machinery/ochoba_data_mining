import json
from dataclasses import dataclass
from datetime import datetime

from src.common.config_loader import ConfigLoader
from src.common.data_base_wrapper import DataBaseWrapper
from src.common.ochoba_api_wrapper import OchobaApiWrapper


class GetSubsites:
    @dataclass
    class Stats:
        request_count: int = 0
        post_count: int = 0
        error_count: int = 0
        requests_since_last_429: int = 0

    def __init__(self):
        config = ConfigLoader.load()
        self.api = OchobaApiWrapper(config["api"])
        self.db = DataBaseWrapper(config["db"])
        self.stats = self.Stats()

    def get_subsites(self):
        print("Started at " + datetime.now().strftime("%H:%M:%S"))
        self.__get_subsites_list("sections")
        self.__get_subsites_list("companies")
        self.db.commit()

    def __get_subsites_list(self, subsite_type):
        response = self.api.execute("subsites_list/" + subsite_type)
        subsites_list = response.json()["result"]
        for subsite_data in subsites_list:
            print(subsite_data)
            self.db.execute_insert(
                """
                    insert into subsites (id, json)
                        values (%s, %s)
                    on conflict (id)
                        do update set json = excluded.json;
                """,
                (subsite_data["id"], json.dumps(subsite_data))
            )


if __name__ == "__main__":
    GetSubsites().get_subsites()
