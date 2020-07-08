from src.common.sql_plot import SqlPlot

SqlPlot().show(
    sql_querys=[
        {
            'query': """
                select date_trunc('week', created) as time_window, count(*)
                from posts
                where type = 1
                group by time_window
                order by time_window
            """, 'label': 'С мемами'
        },
        {
            'query': """
                select date_trunc('week', created) as time_window, count(*)
                from posts
                where type = 1 and subsite_id != 64966
                group by time_window
                order by time_window
            """, 'label': 'Без мемов'
        }
    ],
    title="Количество новых постов за неделю (без репостов и вакансий)",
    x_label="Время",
    y_label="Новые посты за неделю"
)
