import plotly.offline as py
from plotly.graph_objs import *


class Visualizer:
    def __init__(self, raw, auto_open=False):
        self.raw = raw
        self.auto_open = auto_open

        self.MONTH_TYPE_BAR_FILE = "plots/month-type-bar.html"

    def plot_month_type_bar(self):
        # copy the raw data
        df = self.raw.copy()

        # clean up the data
        df['month'] = [ymd[:7] for ymd in df.check_start]
        count = df.groupby(["month", "visa_type"], squeeze=True).count()['__url'].unstack()
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

        py.plot(fig, filename=self.MONTH_TYPE_BAR_FILE, auto_open=self.auto_open)
