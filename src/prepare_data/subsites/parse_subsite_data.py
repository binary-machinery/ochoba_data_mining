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
    print(f"Fetch page #{page} ({offset})")
    result = db.execute_select(
        """
            select id, json from subsites
                order by id
                limit %s offset %s
        """,
        (page_size, offset)
    )
    if len(result) == 0:
        break

    for row in result:
        subsite_id = row[0]
        subsite_data = json.loads(row[1])
        print(subsite_data)
        db.execute_update(
            """
                update subsites
                    set
                        created = to_timestamp(%s),
                        name = %s,
                        type = %s,
                        description = %s,
                        is_verified = %s,
                        is_enable_writing = %s,
                        subscriber_count = %s
                    where id = %s
            """,
            (subsite_data["created"], subsite_data["name"], subsite_data["type"], subsite_data["description"],
             subsite_data["is_verified"], subsite_data["is_enable_writing"], subsite_data["subscribers_count"],
             subsite_id)
        )
    db.commit()
    page += 1

