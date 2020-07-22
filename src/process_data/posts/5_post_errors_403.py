from src.common.sql_plot import SqlPlot

SqlPlot().show(
    sql_queries=[
        {
            'query': """
                select date_trunc('day', estimated_creation_time) as time_window, count(*)
                from post_errors
                where status_code = 403
                    and estimated_creation_time between '2016-01-01 00:00:00.000000' and '2021-01-01 00:00:00.000000'
                group by time_window
                order by time_window
            """
        }
    ],
    title="Посты в скрытых подсайтах",
    x_label="Время",
    y_label="Количество ошибок 403 за день"
)
