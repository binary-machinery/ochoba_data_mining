from src.common.sql_plot import SqlPlot

SqlPlot().show(
    sql_queries=[
        {
            'query': """
                select date_trunc('week', created) as time_window, sum(comments_count)
                from posts
                where type = 1 and created < '2020-07-20'
                group by time_window
                order by time_window
            """
        }
    ],
    title="Количество новых комментариев",
    x_label="Время",
    y_label="Новые комментарии за неделю"
)
