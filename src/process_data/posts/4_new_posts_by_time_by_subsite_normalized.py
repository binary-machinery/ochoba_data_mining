import plotly.graph_objects as go

from src.common.config_loader import ConfigLoader
from src.common.data_base_wrapper import DataBaseWrapper

# https://plotly.com/python/filled-area-plots/

config = ConfigLoader.load()
db = DataBaseWrapper(config["db"])

fig = go.Figure()

subsite_ids, subsite_names = db.fetch_data(
    """
        select subsite_id, subsite_name
        from posts
        where type = 1 and subsite_type = 2
        group by subsite_id, subsite_name
        order by count(id) desc
        limit 19
    """,
    None
)

for (subsite_id, subsite_name) in zip(subsite_ids, subsite_names):
    x, y = db.fetch_data(
        """
            with time_scale as (
                select date_trunc('week', generate_series) as time_window
                from generate_series('2018-06-06'::timestamp, '2020-06-22'::timestamp, '1 week'::interval)
                order by time_window
            )
            select time_scale.time_window, coalesce(data.count, 0) as count
            from time_scale
            left join (
                select date_trunc('week', created) as time_window, count(*)
                from posts
                where type = 1 and subsite_id = %s
                group by time_window
                order by time_window
                ) as data
                on time_scale.time_window = data.time_window
        """,
        (subsite_id,)
    )
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines',
        stackgroup='one',
        groupnorm='percent',
        name=subsite_name
    ))

x, y = db.fetch_data(
    """
        with time_scale as (
            select date_trunc('week', generate_series) as time_window
            from generate_series('2018-06-06'::timestamp, '2020-06-22'::timestamp, '1 week'::interval)
            order by time_window
        )
        select time_scale.time_window, coalesce(data.count, 0) as count
        from time_scale
        left join (
            select date_trunc('week', created) as time_window, count(*)
            from posts
            where type = 1 and subsite_type = 1
            group by time_window
            order by time_window
            ) as data
            on time_scale.time_window = data.time_window
    """,
    None
)
fig.add_trace(go.Scatter(
    x=x,
    y=y,
    mode='lines',
    stackgroup='one',
    groupnorm='percent',
    name='Блоги'
))

fig.update_layout(
    showlegend=True,
    xaxis_type='category',
    yaxis=dict(
        type='linear',
        range=[1, 100],
        ticksuffix='%'))

fig.show()
