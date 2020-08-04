import matplotlib.pyplot as plt

from src.common.config_loader import ConfigLoader
from src.common.data_base_wrapper import DataBaseWrapper

config = ConfigLoader.load()
db = DataBaseWrapper(config["db"])

x, y = db.fetch_data(
    """
        select extract(hour from created) as hour, count(distinct posts.id)
        from posts
        join post_tags
            on posts.id = post_tags.post_id
                and posts.type = 1 and created between '2020-01-01' and '2020-07-01'
                and not posts.is_editorial
                and post_tags.value in ('#лонг', '#лонгрид', '#long', '#longread')
        group by hour
        order by hour
    """, None
)

plt.bar(x, y, color='green')
plt.xlabel("Время (Москва, GMT+3)")
plt.ylabel("Количество лонгов")
plt.title("Количество лонгов (январь-июнь 2020, UGC)")
plt.grid(True, axis='y')

plt.xticks(x)

plt.show()
