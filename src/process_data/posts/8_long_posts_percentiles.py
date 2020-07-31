from src.common.sql_plot import SqlPlot

SqlPlot().show(
    sql_queries=[
        {
            'query': """
                with length_data as (
                    select posts.id, sum(blocks.text_length) as text_length
                    from posts
                    join post_tags tags
                        on posts.id = tags.post_id
                            and posts.type = 1
                            and (tags.value = '#лонг' or tags.value = '#лонгрид')
                    join post_blocks blocks
                        on posts.id = blocks.post_id
                    group by posts.id
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
