from src.common.sql_plot import SqlPlot

SqlPlot().show(
    sql_querys=[
        {
            'query': """
                with data as (
                    select date_trunc('day', date_created) as time_window,
                           count(*) as new_users
                    FROM posts where subsite_id = 87855 AND iseditorial = TRUE AND is_show_thanks = FALSE AND is_filled_by_editors = FALSE
                    group by time_window
                )
                select time_window,
                        sum(new_users) over (
                            order by time_window rows between unbounded preceding and current row
                        ) as total_users
                from data
            """, 'label': '87855'
        },
        {
            'query': """
                with data as (
                    select date_trunc('day', date_created) as time_window,
                           count(*) as new_users
                    FROM posts where subsite_id = 64953 AND iseditorial = TRUE AND is_show_thanks = FALSE AND is_filled_by_editors = FALSE
                    group by time_window
                )
                select time_window,
                        sum(new_users) over (
                            order by time_window rows between unbounded preceding and current row
                        ) as total_users
                from data
            """, 'label': '64953'
        }
    ],
    title="Количество постов",
    x_label="Время",
    y_label="Посты"
)
