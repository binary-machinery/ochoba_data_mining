from src.common.sql_plot import SqlPlot

SqlPlot().show(
    sql_querys=[
        {
            'query': """
                select date_trunc('week', date_created) as time_window, count(*)
                from posts WHERE subsite_id = 64953 AND iseditorial = TRUE AND is_show_thanks = FALSE AND is_filled_by_editors = FALSE
                group by time_window ORDER BY time_window 
            """, 'label': 'games'},
        {
            'query': """
                select date_trunc('week', date_created) as time_window, count(*)
                from posts WHERE subsite_id = 87855 AND iseditorial = TRUE AND is_show_thanks = FALSE AND is_filled_by_editors = FALSE
                group by time_window ORDER BY time_window 
            """, 'label': 'gameindustry'
        }
    ],
    title="Количество новых постов за неделю",
    x_label="Время",
    y_label="Новые посты за неделю"
)
