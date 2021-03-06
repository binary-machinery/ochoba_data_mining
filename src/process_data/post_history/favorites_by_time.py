from src.common.sql_plot import SqlPlot

post_id = 220958

SqlPlot().show(
    sql_queries=[
        {
            'query': f"""
                select request_time, favorites
                from post_history
                where post_id = {post_id}
                order by id
            """
        }
    ],
    title="Закладки",
    x_label="Время",
    y_label="Закладки"
)
