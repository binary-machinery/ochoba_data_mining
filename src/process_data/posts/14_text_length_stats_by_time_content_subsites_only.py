from src.common.config_loader import ConfigLoader
from src.common.data_base_wrapper import DataBaseWrapper
from src.common.sql_plot import SqlPlot

percentiles = [0.75, 0.5, 0.25]

config = ConfigLoader.load()
db = DataBaseWrapper(config["db"])

queries = []
for percentile in percentiles:
    queries.append({
        'query': f"""
            with length_data as (
                select
                       posts.id as post_id,
                       posts.created as created,
                       sum(coalesce(blocks.text_length, 0)) as text_length
                from posts
                join post_blocks blocks
                    on posts.id = blocks.post_id
                        and posts.type = 1
                        and subsite_id in (64953, 64957, 64954, 87855) 
                group by posts.id
            )
            select
                date_trunc('week', created) as time_window,
                percentile_disc({percentile}) within group (order by text_length) as percentile
            from length_data
            where created between '2017-01-01' and '2020-07-19'
            group by time_window
            order by time_window
        """,
        'label': str(int(percentile * 100)) + '-процентиль'
    })

SqlPlot().show(
    sql_queries=queries,
    title="Длина постов (контентная четверка подсайтов)",
    x_label="Время",
    y_label="Процентили"
)
