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

    def __parse_tags(self, post_id, text):
        search_index = 0
        while True:
            match = self.tag_regex.search(text, search_index)
            if match is None:
                break

            parsed_tag = urllib.parse.unquote(match.group(0))
            if len(parsed_tag) >= 3 and not parsed_tag.isdigit():
                self.db.execute_insert(
                    """
                        insert into post_tags (post_id, value, source)
                            values (%s, %s, %s)
                    """,
                    (post_id, parsed_tag.lower(), text)
                )
            search_index = match.end(0)

    def parse(self):
        offset_base = 0
        page_size = 500
        page = 0
        while True:
            offset = offset_base + page_size * page
            print(f"Fetch page #{page} ({offset})")
            result = self.db.execute_select(
                """
                    select id, json from posts
                        order by id
                        limit %s offset %s
                """,
                (page_size, offset)
            )
            if len(result) == 0:
                break

            for row in result:
                post_id = row[0]
                try:
                    post_data = json.loads(row[1])["result"]
                    if "blocks" in post_data:
                        blocks = post_data["blocks"]
                        for block in blocks:
                            block_type = block["type"]
                            block_data = block["data"]
                            text_length = 0
                            if "text" in block_data:
                                text_length = len(block_data["text"])
                                self.__parse_tags(post_id, block_data["text"])
                            if block_type == "list":
                                for item in block_data["items"]:
                                    text_length += len(item)
                                    self.__parse_tags(post_id, item)

                            self.db.execute_insert(
                                """
                                    insert into post_blocks (post_id, type, data, text_length)
                                        values (%s, %s, %s, %s)
                                """,
                                (post_id, block_type, json.dumps(block_data), text_length)
                            )

                    self.db.execute_update(
                        """
                            update posts
                                set
                                    created = to_timestamp(%s),
                                    type = %s,
                                    subsite_id = %s,
                                    subsite_name = %s,
                                    author_id = %s,
                                    author_name = %s,
                                    title = %s,
                                    is_enabled_comments = %s,
                                    is_enabled_likes = %s,
                                    is_repost = %s,
                                    is_show_thanks = %s,
                                    is_filled_by_editors = %s,
                                    is_editorial = %s,
                                    hotness = %s,
                                    comments_count = %s,
                                    favorites_count = %s,
                                    hits_count = %s,
                                    likes_count = %s,
                                    likes_sum = %s
                                where id = %s
                        """,
                        (
                            post_data["date"],
                            post_data["type"],
                            post_data["subsite"]["id"],
                            post_data["subsite"]["name"],
                            post_data["author"]["id"],
                            post_data["author"]["name"],
                            post_data["title"],
                            post_data["isEnabledComments"],
                            post_data["isEnabledLikes"],
                            post_data["isRepost"],
                            post_data.get("is_show_thanks"),
                            post_data.get("is_filled_by_editors"),
                            post_data.get("isEditorial"),
                            post_data.get("hotness"),
                            post_data["commentsCount"],
                            post_data["favoritesCount"],
                            post_data["hitsCount"],
                            post_data["likes"]["count"],
                            post_data["likes"]["summ"],
                            post_id
                        )
                    )

                except Exception:
                    print(f"Exception for post #{post_id}")
                    raise

            page += 1
            self.db.commit()


if __name__ == "__main__":
    ParsePostData().parse()
