import matplotlib.pyplot as plt
import datetime
import matplotlib.animation as animation

from src.common.config_loader import ConfigLoader
from src.common.data_base_wrapper import DataBaseWrapper

ignored_tags = ('#long', '#лонг', '#новости', '#кино', '#фан', '#мнения', '#обзоры', '#разбор', '#опыт', '#игры',
                '#видео', '#сериалы', '#деньги', '#топы', '#истории', '#мобайл', '#киберспорт')

config = ConfigLoader.load()
db = DataBaseWrapper(config["db"])

fig, ax = plt.subplots(figsize=(15, 8))


def draw(date):
    print(date)
    x, y = db.fetch_data(
        f"""
            select post_tags.value, count(distinct posts.id) as cnt
            from posts
            join post_tags
                on posts.id = post_tags.post_id
                    and posts.type = 1
                    and posts.created between '{date}' and to_date('{date}', 'YYYY-MM-DD') + interval '7' day
                    and post_tags.value not in {ignored_tags}  
            group by post_tags.value
            order by cnt desc
            limit 10
        """, None
    )

    y = y[::-1]

    ax.clear()
    ax.barh(x, y)

    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=24)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    ax.set_yticks([])
    plt.box(False)

    ax.text(1, 0.2, date, transform=ax.transAxes, size=60, ha='right')
    for i, (name, value) in enumerate(zip(x, y)):
        ax.text(value, i - 0.13, f"{name} ({value})", size=20, ha='right')

    # plt.show()


dt = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2020, 7, 1)
step = datetime.timedelta(days=1)

dates = []
while dt < end:
    dates.append(dt.strftime('%Y-%m-%d'))
    dt += step

animator = animation.FuncAnimation(fig, func=draw, frames=dates, interval=500, repeat=True)
animator.save("tst.gif", writer='PillowWriter')
