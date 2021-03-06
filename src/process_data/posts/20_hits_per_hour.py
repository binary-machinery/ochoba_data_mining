import matplotlib.pyplot as plt

from src.common.config_loader import ConfigLoader
from src.common.data_base_wrapper import DataBaseWrapper

config = ConfigLoader.load()
db = DataBaseWrapper(config["db"])

x, y = db.fetch_data(
    """
        select extract(hour from created) as hour, avg(hits_count)
        from posts
        where type = 1 and created between '2020-01-01' and '2020-07-01'
        group by hour
        order by hour
    """, None
)

plt.bar(x, y, color='green')
plt.xlabel("Время публикации (Москва, GMT+3)")
plt.ylabel("Среднее количество просмотров")
plt.title("Среднее количество просмотров (январь-июнь 2020)")
plt.grid(True, axis='y')

plt.xticks(x)

plt.show()
