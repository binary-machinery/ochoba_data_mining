from src.common.sql_plot import SqlPlot

SqlPlot().show(
    sql_queries=[
        {
            'query': """
                with long_posts as (
                    select distinct posts.id
                    from posts
                    join post_tags
                        on posts.id = post_tags.post_id
                            and posts.type = 1
                            and post_tags.value in ('#лонг', '#лонгрид', '#longread')
                ), length_data as (
                    select long_posts.id, sum(blocks.text_length) as text_length
                    from long_posts
                    join post_blocks blocks
                        on long_posts.id = blocks.post_id
                    group by long_posts.id
                ), percentiles as (
                    select generate_series as value
                    from generate_series(0, 1, 0.01)
                )
                select
                    percentile_disc(percentiles.value) within group (order by text_length) as percentile,
                    percentiles.value * 100 as probability
                from percentiles cross join length_data
                group by percentiles.value
            """
        }
    ],
    title="Распределение длины лонгов",
    x_label="Количество текстовых символов в посте",
    y_label="Количество постов, %"
)
