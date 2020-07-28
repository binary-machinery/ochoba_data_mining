from src.common.config_loader import ConfigLoader
from src.common.data_base_wrapper import DataBaseWrapper
from src.common.sql_plot import SqlPlot

subsite_ids = [87848]

config = ConfigLoader.load()
db = DataBaseWrapper(config["db"])

queries = []
for subsite_id in subsite_ids:
    subsite_name = db.execute_select_one("select name from subsites where id = %s", (subsite_id,))[0]
    queries.append({
        'query': f"""
            select date_trunc('week', created) as time_window, count(*)
            from posts
            where type = 1 and subsite_id = {subsite_id}
                and created between '2018-06-01' and '2020-07-20'
                and is_editorial = true
            group by time_window
            order by time_window
        """,
        'label': subsite_name + ' (редакция)'
    })
    queries.append({
        'query': f"""
            select date_trunc('week', created) as time_window, count(*)
            from posts
            where type = 1 and subsite_id = {subsite_id}
                and created between '2018-06-01' and '2020-07-20'
                and is_editorial = false
            group by time_window
            order by time_window
        """,
        'label': subsite_name + ' (UGC)'
    })

SqlPlot().show(
    sql_queries=queries,
    title="Количество новых постов за неделю",
    x_label="Время",
    y_label="Новые посты за неделю"
)
