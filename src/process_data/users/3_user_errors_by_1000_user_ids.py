from src.common.sql_plot import SqlPlot

SqlPlot().show(
    sql_query="""
        with all_ids as (
            select generate_series as user_id
            from generate_series(1, (select max(id) from users))
        )
        select
               round(all_ids.user_id, -3) user_id_group,
               count(user_errors.id)
        from all_ids
        left join user_errors
            on all_ids.user_id = user_errors.user_id
        group by user_id_group
        order by user_id_group
    """,
    title="Количество ошибок API",
    x_label="ID пользователя",
    y_label="Количество ошибок на 1000 пользователей"
)