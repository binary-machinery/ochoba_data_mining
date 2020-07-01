import json
import re
import urllib

from src.common.config_loader import ConfigLoader
from src.common.data_base_wrapper import DataBaseWrapper


class ParsePostData:
    def __init__(self):
        config = ConfigLoader.load()
        self.db = DataBaseWrapper(config["db"])
        self.tag_regex = re.compile(config["api"]["tag_regex"])

    def parse(self):
        page_size = 500
        page = 0
        while True:
            print("Fetch page #{0} ({1})".format(page, page_size * page))
            result = self.db.execute_select(
                """
                    select json from posts
                        order by id
                        limit %s offset %s
                """,
                (page_size, page_size * page)
            )
            if len(result) == 0:
                break

            for row in result:
                post_data = json.loads(row[0])["result"]

                if "entryContent" in post_data:
                    search_index = 0
                    parsed_tags = []
                    while True:
                        match = self.tag_regex.search(post_data["entryContent"]["html"], search_index)
                        if match is None:
                            break

                        parsed_tags.append(urllib.parse.unquote(match.group(1)))
                        search_index = match.end(1)

                    post_data["parsed_tags"] = parsed_tags

                text_length = 0
                media_count = 0
                if "blocks" in post_data:
                    for block in post_data["blocks"]:
                        if block["type"] in ["media", "video"]:
                            media_count += 1
                        elif block["type"] in ["text", "header", "incut", "quote"]:
                            text_length += len(block["data"]["text"])

                # self.db.execute_update(
                #     """
                #         update posts
                #             set
                #                 created = to_timestamp(%s),
                #                 name = %s,
                #                 type = %s,
                #                 karma = %s,
                #                 is_plus = %s,
                #                 is_verified = %s,
                #                 is_available_for_messenger = %s,
                #                 entries_count = %s,
                #                 comments_count = %s,
                #                 favorites_count = %s,
                #                 subscribers_count = %s
                #             where id = %s
                #     """,
                #     (post_data["created"], post_data["name"], post_data["type"], post_data["karma"],
                #      post_data["is_plus"], post_data["is_verified"], post_data["isAvailableForMessenger"],
                #      post_data["counters"]["entries"], post_data["counters"]["comments"],
                #      post_data["counters"]["favorites"], post_data["subscribers_count"],
                #      post_data["id"])
                # )

            page += 1
            self.db.commit()


if __name__ == "__main__":
    ParsePostData().parse()
