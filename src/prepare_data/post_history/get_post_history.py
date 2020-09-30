import json
import time
from datetime import datetime

from src.common.config_loader import ConfigLoader
from src.common.data_base_wrapper import DataBaseWrapper
from src.common.ochoba_api_wrapper import OchobaApiWrapper

post_id = 221596
request_interval_minutes = 1

config = ConfigLoader.load()
api = OchobaApiWrapper(config["api"])
db = DataBaseWrapper(config["db"])

print(datetime.now().strftime("%H:%M:%S") + ": Started")

while True:
    response = api.execute("entry/" + str(post_id))
    print(datetime.now().strftime("%H:%M:%S") + ": Got " + str(response.status_code))
    if response.status_code == 200:
        db.execute_insert(
            """
                insert into post_history (post_id, request_time, json)
                    values (%s, %s, %s);
            """,
            (post_id, datetime.now(), json.dumps(response.json()))
        )
        db.commit()

    time.sleep(60 * request_interval_minutes)
