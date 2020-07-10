import plotly.graph_objects as go

from src.common.config_loader import ConfigLoader
from src.common.data_base_wrapper import DataBaseWrapper

# https://plotly.com/python/filled-area-plots/

config = ConfigLoader.load()
db = DataBaseWrapper(config["db"])

fig = go.Figure()

subsite_ids, subsite_names = db.fetch_data(
    """
        with data as (
            select id,
                   created,
                   case when subsite_type = 1 then 0 else subsite_id end         as subsite_id,
                   case when subsite_type = 1 then 'Блоги' else subsite_name end as subsite_name,
                   subsite_type
            from posts
            where type = 1
        )
        select subsite_id, subsite_name
        from data
        where subsite_id != 0
        group by subsite_id, subsite_name
        order by count(id) desc
        limit 19
    """,
    None
)

for (subsite_id, subsite_name) in zip(subsite_ids, subsite_names):
    x, y = db.fetch_data(
        """
            with time_windows as (
                select date_trunc('week', created) as time_window
                from posts
                where created between '2018-06-06 00:00:00.000000' and '2020-06-22 00:00:00.000000'
                group by time_window
                order by time_window
            )
            select time_windows.time_window, coalesce(data.count, 0) as count
            from time_windows
            left join (
                select date_trunc('week', created) as time_window, count(*)
                from posts
                where type = 1
                  and subsite_id = %s
                group by time_window
                order by time_window
                ) as data
                on time_windows.time_window = data.time_window
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
        with time_windows as (
            select date_trunc('week', created) as time_window
            from posts
            where created between '2018-06-08 00:00:00.000000' and '2020-06-22 00:00:00.000000'
            group by time_window
            order by time_window
        )
        select time_windows.time_window, coalesce(data.count, 0) as count
        from time_windows
        left join (
            select date_trunc('week', created) as time_window, count(*)
            from posts
            where type = 1 and subsite_type = 1
            group by time_window
            order by time_window
            ) as data
            on time_windows.time_window = data.time_window
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
