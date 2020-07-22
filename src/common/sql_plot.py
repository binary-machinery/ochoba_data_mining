import matplotlib.pyplot as plot

from src.common.config_loader import ConfigLoader
from src.common.data_base_wrapper import DataBaseWrapper


class SqlPlot:
    def __init__(self):
        config = ConfigLoader.load()
        self.db = DataBaseWrapper(config["db"])

    def show(self, sql_queries, title, x_label, y_label):
        show_legend = False
        for sql_query in sql_queries:
            data = self.db.execute_select(sql_query.get('query'), None)
            x = []
            y = []
            for row in data:
                x.append(row[0])
                y.append(row[1])

            label = sql_query.get('label')
            plot.plot(x, y, label=label)
            show_legend |= label is not None

        plot.title(title)
        plot.xlabel(x_label)
        plot.ylabel(y_label)
        plot.grid(True)

        if show_legend:
            plot.legend()

        plot.show()
