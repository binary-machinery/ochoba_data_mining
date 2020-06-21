from src.common.sql_plot import SqlPlot

SqlPlot().show(
    sql_query="""
        select karma, count(*)
        from users
        where karma < 0
        group by karma
    """,
    title="Количество ошибок API",
    x_label="ID пользователя",
    y_label="Количество ошибок на 1000 пользователей"
)