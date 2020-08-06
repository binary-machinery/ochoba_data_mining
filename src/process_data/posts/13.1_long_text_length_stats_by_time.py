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
            with long_posts as (
                select distinct posts.id, created
                from posts
                join post_tags
                    on posts.id = post_tags.post_id
                        and posts.type = 1
                        and post_tags.value in ('#лонг', '#лонгрид', '#longread')
            ), length_data as (
                select long_posts.id, created, sum(blocks.text_length) as text_length
                from long_posts
                join post_blocks blocks
                    on long_posts.id = blocks.post_id
                group by long_posts.id, created
            )
            select
                date_trunc('week', created) as time_window,
                percentile_disc({percentile}) within group (order by text_length) as percentile
            from length_data
            where created between '2019-02-01' and '2020-07-19'
            group by time_window
            order by time_window
        """,
        'label': str(int(percentile * 100)) + '-процентиль'
    })

SqlPlot().show(
    sql_queries=queries,
    title="Длина лонгов",
    x_label="Время",
    y_label="Процентили"
)
