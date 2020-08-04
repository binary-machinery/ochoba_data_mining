from src.common.sql_plot import SqlPlot

tag_group = ('#thelastofus', '#thelastofus2', '#tlou', '#tlou2')

SqlPlot().show(
    sql_queries=[{
        'query': f"""
        select date_trunc('week', posts.created) as time_window, count(distinct posts.id)
        from posts
        join post_tags
            on posts.id = post_tags.post_id
                and posts.type = 1
                and posts.created > '2019-01-01'
                and post_tags.value in {tag_group}
        group by time_window
        order by time_window
    """, 'label': tag_group
    }],
    title="Количество новых постов за неделю с тегами",
    x_label="Время",
    y_label="Новые посты за неделю"
)
