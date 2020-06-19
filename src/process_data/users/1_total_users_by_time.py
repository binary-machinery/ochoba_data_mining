from src.common.sql_plot import SqlPlot

SqlPlot().show(
    sql_query="""
        with data as (
            select date_trunc('day', created) as time_window,
                   count(*) as new_users
            from users
            group by time_window
        )
        select time_window,
                sum(new_users) over (
                    order by time_window rows between unbounded preceding and current row
                ) as total_users
        from data
    """,
    title="Количество пользователей",
    x_label="Время",
    y_label="Пользователи"
)
