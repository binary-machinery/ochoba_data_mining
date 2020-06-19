import matplotlib.pyplot as plot

from src.common.config_loader import ConfigLoader
from src.common.data_base_wrapper import DataBaseWrapper


class SqlPlot:
    def __init__(self):
        config = ConfigLoader.load()
        self.db = DataBaseWrapper(config["db"])

    def show(self, sql_query, title, x_label, y_label):
        data = self.db.execute_select(sql_query, None)
        x = []
        y = []
        for row in data:
            x.append(row[0])
            y.append(row[1])

        plot.plot(x, y)

        plot.title(title)
        plot.xlabel(x_label)
        plot.ylabel(y_label)
        plot.grid(True)

        plot.show()
