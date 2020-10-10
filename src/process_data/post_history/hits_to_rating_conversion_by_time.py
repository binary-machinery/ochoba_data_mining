from src.common.sql_plot import SqlPlot

post_id = 220958

SqlPlot().show(
    sql_queries=[
        {
            'query': f"""
                with data as (
                    select date_trunc('hour', request_time) as hours,
                           min(request_time)                as request_time,
                           min(hits)                        as hits,
                           min(rating)                      as rating
                    from post_history
                    group by hours
                    order by hours
                ),
                     delta_data as (
                         select request_time,
                                (hits - coalesce(lag(hits, 1) over (order by hours), 0))::float                      as d_hits,
                                (rating - coalesce(lag(rating, 1) over (order by hours), 0))::float                  as d_rating,
                                extract(epoch from request_time - lag(request_time, 1) over (order by hours)) / 3600 as d_time
                         from data
                     )
                select request_time,
                       case when d_hits != 0 then d_rating / d_hits / d_time else 0 end as rate
                from delta_data
                where request_time < '2020-10-03'
            """
        }
    ],
    title="Конверсия просмотров в рейтинг",
    x_label="Время",
    y_label="Коэффициент"
)
