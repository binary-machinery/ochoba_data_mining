from src.common.sql_plot import SqlPlot

SqlPlot().show(
    sql_querys=[
        {
            'query': """
                select date_trunc('week', created) as time_window, count(*)
                from posts
                where type = 1 and subsite_type = 1 and created < '2020-06-29 00:00:00.000000'
                group by time_window
                order by time_window
            """, 'label': 'Блоги'
        },
        {
            'query': """
                select date_trunc('week', created) as time_window, count(*)
                from posts
                where type = 1 and subsite_id = 64966 and created < '2020-06-29 00:00:00.000000'
                group by time_window
                order by time_window
            """, 'label': 'Мемы'
        },
        {
            'query': """
                select date_trunc('week', created) as time_window, count(*)
                from posts
                where type = 1 and subsite_id = 64961 and created < '2020-06-29 00:00:00.000000'
                group by time_window
                order by time_window
            """, 'label': 'Вопросы'
        },
        {
            'query': """
                select date_trunc('week', created) as time_window, count(*)
                from posts
                where type = 1 and subsite_id = 64953 and created < '2020-06-29 00:00:00.000000'
                group by time_window
                order by time_window
            """, 'label': 'Игры'
        },
        {
            'query': """
                select date_trunc('week', created) as time_window, count(*)
                from posts
                where type = 1 and subsite_id = 64955 and created < '2020-06-29 00:00:00.000000'
                group by time_window
                order by time_window
            """, 'label': 'Офтоп'
        },
        {
            'query': """
                select date_trunc('week', created) as time_window, count(*)
                from posts
                where type = 1 and subsite_id = 87855 and created < '2020-06-29 00:00:00.000000'
                group by time_window
                order by time_window
            """, 'label': 'Индустрия игр'
        },
        {
            'query': """
                select date_trunc('week', created) as time_window, count(*)
                from posts
                where type = 1 and subsite_id = 64954 and created < '2020-06-29 00:00:00.000000'
                group by time_window
                order by time_window
            """, 'label': 'Gamedev'
        },
        {
            'query': """
                select date_trunc('week', created) as time_window, count(*)
                from posts
                where type = 1 and subsite_id = 64957 and created < '2020-06-29 00:00:00.000000'
                group by time_window
                order by time_window
            """, 'label': 'Кино и сериалы'
        }
    ],
    title="Количество новых постов за неделю по подсайтам",
    x_label="Время",
    y_label="Новые посты за неделю"
)
