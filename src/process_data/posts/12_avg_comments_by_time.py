from src.common.sql_plot import SqlPlot

SqlPlot().show(
    sql_queries=[
        {
            'query': """
                select date_trunc('week', created) as time_window, avg(comments_count)
                from posts
                where type = 1 and created between '2016-06-01' and '2020-07-19'
                group by time_window
                order by time_window
            """
        }
    ],
    title="Среднее количество комментариев на пост",
    x_label="Время",
    y_label="Среднее количество комментариев на пост"
)
