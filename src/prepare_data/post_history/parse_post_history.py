import json

from src.common.config_loader import ConfigLoader
from src.common.data_base_wrapper import DataBaseWrapper

config = ConfigLoader.load()
db = DataBaseWrapper(config["db"])

offset_base = 0
page_size = 500
page = 0
while True:
    offset = offset_base + page_size * page
    result = db.execute_select(
        """
            select id, json from post_history
                order by id
                limit %s offset %s
        """,
        (page_size, offset)
    )
    if len(result) == 0:
        break

    for row in result:
        record_id = row[0]
        print("parsing " + str(record_id))

        post_data = json.loads(row[1])["result"]
        db.execute_update(
            """
                update post_history
                    set
                        hits = %s,
                        rating = %s,
                        comments = %s,
                        favorites = %s
                    where id = %s
            """,
            (
                post_data["hitsCount"],
                post_data["likes"]["summ"],
                post_data["commentsCount"],
                post_data["favoritesCount"],
                record_id
            )
        )

    page += 1
    db.commit()
