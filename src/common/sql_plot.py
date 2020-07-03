import matplotlib.pyplot as plot

from src.common.config_loader import ConfigLoader
from src.common.data_base_wrapper import DataBaseWrapper


class SqlPlot:
    def __init__(self):
        config = ConfigLoader.load()
        self.db = DataBaseWrapper(config["db"])

    def show(self, sql_querys, title, x_label, y_label):
        for sql_query in sql_querys:
            data = self.db.execute_select(sql_query.get('query'), None)
            x = []
            y = []
            for row in data:
                x.append(row[0])
                y.append(row[1])

            plot.plot(x, y, label=sql_query.get('label'))

        plot.title(title)
        plot.xlabel(x_label)
        plot.ylabel(y_label)
        plot.grid(True)
        plot.legend()
        plot.show()
