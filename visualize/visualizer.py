import plotly.offline as py
from plotly.graph_objs import *


class Visualizer:
    def __init__(self, raw, auto_open=False):
        self.raw = raw
        self.auto_open = auto_open

        self.MONTH_TYPE_COLUMN = "visa_type"
        self.MONTH_TYPE_BAR_FILE = "plots/month-type-bar.html"

        self.MONTH_CONSULATE_COLUMN = "visa_consulate"
        self.MONTH_CONSULATE_BAR_FILE = "plots/month-consulate-bar.html"

    def plot_month_bar(self, category="visa_type", filename="plots/month-type-bar.html"):
        # copy the raw data
        df = self.raw.copy()

        # clean up the data
        df['month'] = [str(ymd)[:7] for ymd in df.check_start]
        count = df.groupby(["month", category], squeeze=True).count()['__url'].unstack()
        count = count.fillna(0)

        # generate the visualization output
        data = []
        for k in count.keys():
            data.append(
                Bar(
                    x=count.index,
                    y=count[k],
                    name=k)
            )

        _layout = Layout(
            barmode='stack'
        )

        fig = Figure(data=data, layout=_layout)

        py.plot(fig, filename=filename, auto_open=self.auto_open)

    def plot_month_type_bar(self):
        self.plot_month_bar(self.MONTH_TYPE_COLUMN, self.MONTH_TYPE_BAR_FILE)

    def plot_month_consulate_bar(self):
        self.plot_month_bar(self.MONTH_CONSULATE_COLUMN, self.MONTH_CONSULATE_BAR_FILE)
