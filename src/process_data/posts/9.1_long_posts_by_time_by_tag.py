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
                        and posts.created between '2016-06-01' and '2020-07-20'
                        and tags.value in ('#лонг', '#лонгрид', '#longread')
                group by time_window
                order by time_window
            """, 'label': "#лонг, #лонгрид, #longread"
        },
        {
            'query': """
                select date_trunc('week', created) as time_window, count(distinct posts.id)
                from posts
                join post_tags tags
                    on posts.id = tags.post_id
                        and posts.type = 1
                        and posts.created between '2016-06-01' and '2020-07-20'
                        and tags.value in ('#лонг', '#лонгрид', '#long', '#longread')
                group by time_window
                order by time_window
            """, 'label': "#long"
        }
    ],
    title="Новые лонги",
    x_label="Время",
    y_label="Новые лонги за неделю"
)
