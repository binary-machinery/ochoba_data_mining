import json
import time
from datetime import datetime

from src.common.config_loader import ConfigLoader
from src.common.data_base_wrapper import DataBaseWrapper
from src.common.ochoba_api_wrapper import OchobaApiWrapper


class GetPosts:
    class Stats:
        def __init__(self):
            self.request_count = 0
            self.post_count = 0
            self.error_count = 0
            self.requests_since_last_429 = 0

    def __init__(self):
        config = ConfigLoader.load()
        self.api = OchobaApiWrapper(config["api"])
        self.db = DataBaseWrapper(config["db"])
        self.stats = self.Stats()

    def get_posts(self):
        print("Started at " + datetime.now().strftime("%H:%M:%S"))
        for post_id in range(1, 164000):
            if self.stats.request_count % 100 == 0:
                self.db.commit()
                print("{0}: {1} requests processed ({2} posts, {3} errors)"
                      .format(datetime.now().strftime("%H:%M:%S"),
                              self.stats.request_count,
                              self.stats.post_count,
                              self.stats.error_count))

            self.__get_post(post_id)

        self.db.commit()

    def __get_post(self, post_id):
        response = self.api.execute("entry/" + str(post_id))
        if response.status_code == 429:
            # Too Many Requests
            print(datetime.now().strftime("%H:%M:%S")
                  + ": 429 Too Many Requests. Requests processed since last 429 error: "
                  + str(self.stats.requests_since_last_429)
                  + ". Wait for 60 seconds and repeat")
            self.stats.requests_since_last_429 = 0
            time.sleep(60)
            self.__get_post(post_id)
            return

        response_json = response.json()
        print(str(response.status_code) + ": " + str(response_json))

        if "error" in response_json:
            self.db.execute_insert(
                """
                    insert into post_errors (post_id, status_code, response)
                        values (%s, %s, %s);
                """,
                (post_id, response.status_code, json.dumps(response_json))
            )
            self.stats.error_count += 1

        else:
            self.db.execute_insert(
                """
                    insert into posts (id, json)
                        values (%s, %s)
                    on conflict (id)
                        do update set json = excluded.json;
                """,
                (post_id, json.dumps(response_json))
            )
            self.stats.post_count += 1

        self.stats.request_count += 1
        self.stats.requests_since_last_429 += 1


if __name__ == "__main__":
    GetPosts().get_posts()
