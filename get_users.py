import json
import pathlib
import time
from datetime import datetime

from data_base_wrapper import DataBaseWrapper
from ochoba_api_wrapper import OchobaApiWrapper


class GetUsers:
    class Stats:
        def __init__(self):
            self.request_count = 0
            self.user_count = 0
            self.error_count = 0
            self.requests_since_last_429 = 0

    def __init__(self):
        script_path = pathlib.Path(__file__).parent.absolute()
        with open(str(script_path) + "/config.json") as json_file:
            config = json.load(json_file)

        self.api = OchobaApiWrapper(config["api"])
        self.db = DataBaseWrapper(config["db"])
        self.stats = self.Stats()

    def get_users(self):
        print("Started at " + datetime.now().strftime("%H:%M:%S"))
        for user_id in range(1, 250000):
            if self.stats.request_count % 100 == 0:
                self.db.commit()
                print("{0}: {1} requests processed ({2} users, {3} errors)"
                      .format(datetime.now().strftime("%H:%M:%S"),
                              self.stats.request_count,
                              self.stats.user_count,
                              self.stats.error_count))

            self.__get_user(user_id)

        self.db.commit()

    def __get_user(self, user_id):
        response = self.api.execute("user/" + str(user_id))
        if response.status_code == 429:
            # Too Many Requests
            print(datetime.now().strftime("%H:%M:%S")
                  + ": 429 Too Many Requests. Requests processed since last 429 error: "
                  + str(self.stats.requests_since_last_429)
                  + ". Wait for 60 seconds and repeat")
            self.stats.requests_since_last_429 = 0
            time.sleep(60)
            self.__get_user(user_id)
            return

        response_json = response.json()
        print(str(response.status_code) + ": " + str(response_json))

        if "error" in response_json:
            self.db.execute_insert(
                """
                    insert into user_errors (user_id, status_code, response)
                        values (%s, %s, %s);
                """,
                (user_id, response.status_code, json.dumps(response_json))
            )
            self.stats.error_count += 1

        else:
            self.db.execute_insert(
                """
                    insert into users (id, json)
                        values (%s, %s)
                    on conflict (id)
                        do update set json = excluded.json;
                """,
                (user_id, json.dumps(response_json))
            )
            self.stats.user_count += 1

        self.stats.request_count += 1
        self.stats.requests_since_last_429 += 1


if __name__ == "__main__":
    GetUsers().get_users()
