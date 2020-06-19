from src.common.sql_plot import SqlPlot

SqlPlot().show(
    sql_query="""
        select date_trunc('week', created) as time_window, count(*)
        from users
        group by time_window
    """,
    title="Количество новых пользователей за неделю",
    x_label="Время",
    y_label="Новые пользователи"
)
