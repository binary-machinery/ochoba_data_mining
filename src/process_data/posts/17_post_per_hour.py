import matplotlib.pyplot as plt

from src.common.config_loader import ConfigLoader
from src.common.data_base_wrapper import DataBaseWrapper

config = ConfigLoader.load()
db = DataBaseWrapper(config["db"])

x, y = db.fetch_data(
    """
        select extract(hour from created) as hour, count(*)
        from posts
        where type = 1 and created between '2020-01-01' and '2020-07-01' 
            and not is_editorial and subsite_type = 2
        group by hour
        order by hour
    """, None
)

plt.bar(x, y, color='green')
plt.xlabel("Время (Москва, GMT+3)")
plt.ylabel("Количество постов")
plt.title("Количество постов (январь-июнь 2020, UGC, подсайты)")
plt.grid(True, axis='y')

plt.xticks(x)

plt.show()
