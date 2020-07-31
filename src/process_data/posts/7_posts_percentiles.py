from src.common.sql_plot import SqlPlot

SqlPlot().show(
    sql_queries=[
        {
            'query': """
                with length_data as (
                    select
                           posts.id as post_id,
                           sum(coalesce(blocks.text_length, 0)) as text_length
                    from posts
                    left join post_blocks blocks
                        on posts.id = blocks.post_id
                            and posts.type = 1
                    group by posts.id
                ), percentiles as (
                    select generate_series as value
                    from generate_series(0, 0.95, 0.01)
                )
                select
                    percentile_disc(percentiles.value) within group (order by text_length),
                    percentiles.value * 100
                from percentiles cross join length_data
                where text_length < 341961
                group by percentiles.value
            """
        }
    ],
    title="Распределение длины постов",
    x_label="Количество текстовых символов в посте",
    y_label="Количество постов, %"
)
