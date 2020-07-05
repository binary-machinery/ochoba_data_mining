import time
from datetime import datetime
from dataclasses import dataclass

from src.common.config_loader import ConfigLoader
from src.common.data_base_wrapper import DataBaseWrapper
from src.common.ochoba_api_wrapper import OchobaApiWrapper

'''
author: https://github.com/alekxeyuk
source: https://github.com/binary-machinery/ochoba_data_mining/pull/1
might be outdated
'''


class GetSubsiteTimeline:
    @dataclass
    class Stats():
        request_count: int = 0
        post_count: int = 0
        error_count: int = 0
        requests_since_last_429: int = 0

    def __init__(self):
        config = ConfigLoader.load()
        self.api = OchobaApiWrapper(config["api"])
        self.db = DataBaseWrapper(config["db"])
        self.stats = self.Stats()
        self.offset = 1
        self.count = 50
        self.subsite_id = 203796

    @staticmethod
    def __time():
        return datetime.now().strftime("%H:%M:%S")

    def get_posts(self):
        print(f"Started at {self.__time()}")
        timeline = self.__get_timeline(self.subsite_id, 'new', self.count, self.offset)
        while timeline:
            print(f'{len(timeline)}/{self.offset}')
            parsed_timeline = self.__parse_timeline(timeline)
            self.__db_insert(parsed_timeline)

            if self.stats.request_count % 10 == 0:
                self.db.commit()
                print(f'{self.__time()}: {self.stats.request_count} requests processed ({self.stats.post_count} posts, {self.stats.error_count} errors)')
            self.offset += self.count
            timeline = self.__get_timeline(self.subsite_id, 'new', self.count, self.offset)

        self.db.commit()

    def __db_insert(self, parsed_timeline: list):
        for post in parsed_timeline:
            self.db.execute_insert(
                """
                    insert into posts (id, commentscount, favoritescount, hitscount, likescount, date_created, subsite_id, is_show_thanks, is_filled_by_editors, iseditorial)
                        values (%s, %s, %s, %s, %s, to_timestamp(%s), %s, %s, %s, %s)
                    on conflict (id)
                        do update set date_created = excluded.date_created;
                """,
                ([*post.values()])
            )
            self.stats.post_count += 1

        self.stats.request_count += 1
        self.stats.requests_since_last_429 += 1

    def __parse_timeline(self, timeline: list) -> list:
        parsed = [dict(
            entry_id=post.get('id'),
            commentsCount=post.get('commentsCount'),
            favoritesCount=post.get('favoritesCount'),
            hitsCount=post.get('hitsCount'),
            likesCount=post.get('likes').get('count', 0),
            date_created=post.get('date'),
            subsite_id=self.subsite_id,
            is_show_thanks=post.get('is_show_thanks'),
            is_filled_by_editors=post.get('is_filled_by_editors'),
            isEditorial=post.get('isEditorial')) for post in timeline if not post.get('isRepost')]
        return parsed

    def __get_timeline(self, subsite: int, sorting: str = 'new', count: int = 50, offset: int = 0) -> list:
        response = self.api.execute(f"subsite/{subsite}/timeline/{sorting}?count={count}&offset={offset}")
        if response.status_code == 429:
            print(f'{self.__time()}: 429 Too Many Requests. Requests processed since last 429 error: {self.stats.requests_since_last_429}')
            self.stats.requests_since_last_429 = 0
            time.sleep(60)
            return self.__get_timeline(subsite, sorting, count, offset)

        response_json = response.json()
        print(f"__get_timeline:{response.status_code}: {self.__time()}")

        return response_json.get('result')


if __name__ == "__main__":
    GetSubsiteTimeline().get_posts()
