from src.common.sql_plot import SqlPlot

SqlPlot().show(
    sql_queries=[
        {
            'query': """
                select date_trunc('week', created) as time_window, count(distinct posts.id)
                from posts
                join post_tags tags
                    on posts.id = tags.post_id
                        and posts.type = 1
                        and posts.created between '2019-01-21' and '2020-07-20'
                        and posts.is_editorial = true
                        and (tags.value = '#лонг' or tags.value = '#лонгрид')
                group by time_window
                order by time_window
            """, 'label': "Лонги (редакция)"
        },
        {
            'query': """
                select date_trunc('week', created) as time_window, count(distinct posts.id)
                from posts
                join post_tags tags
                    on posts.id = tags.post_id
                        and posts.type = 1
                        and posts.created between '2019-01-21' and '2020-07-20'
                        and posts.is_editorial = false
                        and (tags.value = '#лонг' or tags.value = '#лонгрид')
                group by time_window
                order by time_window
            """, 'label': "Лонги (UGC)"
        },
    ],
    title="Новые лонги",
    x_label="Время",
    y_label="Новые лонги за неделю"
)
