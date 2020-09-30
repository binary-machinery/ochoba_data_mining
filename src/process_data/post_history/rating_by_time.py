from src.common.sql_plot import SqlPlot

post_id = 221596

SqlPlot().show(
    sql_queries=[
        {
            'query': f"""
                select request_time, rating
                from post_history
                where post_id = {post_id}
                order by id
            """
        }
    ],
    title="Рейтинг",
    x_label="Время",
    y_label="Рейтинг"
)
