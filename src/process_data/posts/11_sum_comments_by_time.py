from src.common.sql_plot import SqlPlot

SqlPlot().show(
    sql_queries=[
        {
            'query': """
                select date_trunc('week', created) as time_window, sum(comments_count)
                from posts
                where type = 1 and created between '2016-06-01' and '2020-07-19'
                group by time_window
                order by time_window
            """
        }
    ],
    title="Количество новых комментариев",
    x_label="Время",
    y_label="Новые комментарии за неделю"
)
