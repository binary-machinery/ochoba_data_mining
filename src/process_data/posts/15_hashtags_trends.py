from src.common.sql_plot import SqlPlot

tags = ['#cyberpunk2077']

queries = []
for tag in tags:
    if type(tag) is tuple:
        queries.append({
            'query': f"""
            select date_trunc('week', posts.created) as time_window, count(distinct posts.id)
            from posts
            join post_tags
                on posts.id = post_tags.post_id
                    and posts.type = 1
                    and posts.created > '2018-01-01'
                    and post_tags.value in {tag}
            group by time_window
            order by time_window
        """, 'label': tag
        })
    else:
        queries.append({
            'query': f"""
            select date_trunc('week', posts.created) as time_window, count(distinct posts.id)
            from posts
            join post_tags
                on posts.id = post_tags.post_id
                    and posts.type = 1
                    and posts.created > '2018-01-01'
                    and post_tags.value = '{tag}'
            group by time_window
            order by time_window
        """, 'label': tag
        })

SqlPlot().show(
    sql_queries=queries,
    title="Количество новых постов за неделю с тегами",
    x_label="Время",
    y_label="Новые посты за неделю"
)
