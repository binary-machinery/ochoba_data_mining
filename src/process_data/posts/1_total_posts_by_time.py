from src.common.sql_plot import SqlPlot

SqlPlot().show(
    sql_querys=[
        {
            'query': """
                with data as (
                    select date_trunc('week', created) as time_window,
                           count(*) as new_posts
                    from posts
                    group by time_window
                )
                select time_window,
                        sum(new_posts) over (
                            order by time_window rows between unbounded preceding and current row
                        ) as total_posts
                from data
            """
        }
    ],
    title="Количество постов",
    x_label="Время",
    y_label="Посты"
)
