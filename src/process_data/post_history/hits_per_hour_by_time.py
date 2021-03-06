from src.common.sql_plot import SqlPlot

post_id = 220958

SqlPlot().show(
    sql_queries=[
        {
            'query': f"""
                with data as (
                    select date_trunc('hour', request_time) as hours,
                           min(request_time)                as request_time,
                           min(hits)                        as hits
                    from post_history
                    group by hours
                    order by hours
                )
                select request_time,
                       coalesce((hits - coalesce(lag(hits, 1) over (order by hours), 0)) 
                            / (extract(epoch from request_time - lag(request_time, 1) over (order by hours)) / 3600), 0)
                from data
            """
        }
    ],
    title="Просмотры в час",
    x_label="Время",
    y_label="Просмотры в час"
)
