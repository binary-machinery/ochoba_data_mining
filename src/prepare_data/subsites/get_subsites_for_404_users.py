import json
import time
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

        errors = self.db.execute_select(
            """
                select user_id
                from user_errors
                where status_code = 404
            """,
            None
        )

        for error in errors:
            user_id = error[0]
            subsite_data = self.db.execute_select_one(
                """
                    select id
                    from subsites
                    where id = %s
                """,
                (user_id,)
            )
            if subsite_data is None:
                self.__get_subsite(user_id)

    def __get_subsite(self, subsite_id):
        response = self.api.execute("subsite/" + str(subsite_id))
        if response.status_code == 429:
            # Too Many Requests
            print(datetime.now().strftime("%H:%M:%S")
                  + ": 429 Too Many Requests. Requests processed since last 429 error: "
                  + str(self.stats.requests_since_last_429)
                  + ". Wait for 60 seconds and repeat")
            self.stats.requests_since_last_429 = 0
            time.sleep(60)
            self.__get_subsite(subsite_id)
            return

        print(str(subsite_id) + ": " + str(response.status_code) + ": " + str(response.json()))
        if response.status_code == 200:
            self.db.execute_insert(
                """
                    insert into subsites (id, json)
                        values (%s, %s)
                    on conflict (id)
                        do update set json = excluded.json;
                """,
                (subsite_id, json.dumps(response.json()["result"]))
            )
            self.db.commit()


if __name__ == "__main__":
    GetSubsites().get_subsites()
