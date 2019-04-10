import plotly.offline as py
from plotly.graph_objs import *
from datetime import datetime


class Visualizer:
    def __init__(self, raw, auto_open=False):
        self.raw = raw
        self.auto_open = auto_open

        self.CHECK_LENGTH_FILE = "docs/resource/html/check-length.html"

        self.MONTH_TYPE_COLUMN = "visa_type"
        self.MONTH_TYPE_BAR_FILE = "docs/resource/html/month-type-bar.html"

        self.MONTH_CONSULATE_COLUMN = "visa_consulate"
        self.MONTH_CONSULATE_BAR_FILE = "docs/resource/html/month-consulate-bar.html"

    def plot_check_length(self, rolling_window=28):
        # copy the raw data
        df = self.raw.copy()

        # calculated the check length
        clear = df.query("check_end != '0000-00-00'")
        check_len = []
        for i in range(len(clear)):
            start = datetime.strptime(clear.check_start.iloc[i], "%Y-%m-%d")
            end = datetime.strptime(clear.check_end.iloc[i], "%Y-%m-%d")
            check_len.append((end - start).days)
        clear['check_len'] = check_len
        clear = clear.reset_index()
        clear_pivot = clear.pivot(index="index", columns='check_end', values='check_len')

        mean = clear_pivot.quantile(0.5).rolling(rolling_window, center=True).mean()
        upper_bound = clear_pivot.quantile(0.90).rolling(rolling_window, center=True).mean()
        lower_bound = clear_pivot.quantile(0.10).rolling(rolling_window, center=True).mean()

        # plot and save

        upper_bound = Scatter(
            name='Upper Bound',
            x=upper_bound.index,
            y=upper_bound,
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty')

        trace = Scatter(
            name='Measurement',
            x=mean.index,
            y=mean,
            mode='lines',
            line=dict(color='rgb(31, 119, 180)'),
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty')

        lower_bound = Scatter(
            name='Lower Bound',
            x=lower_bound.index,
            y=lower_bound,
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines')

        # Trace order can be important
        # with continuous error bars
        data = [lower_bound, trace, upper_bound]

        layout = Layout(
            yaxis=dict(title='Waiting time (days)', autorange=True),
            title='Waiting time and 90%/10% error bars',
            showlegend=False)

        fig = Figure(
            data=data,
            layout=layout
        )
        # Plot and embed in ipython notebook!
        py.plot(fig, filename=self.CHECK_LENGTH_FILE, auto_open=self.auto_open)

    def plot_month_bar(self, category="visa_type", filename="plots/month-type-bar.html"):
        # copy the raw data
        df = self.raw.copy()

        # clean up the data
        df['month'] = [str(ymd)[:7] for ymd in df.check_start]
        count = df.groupby(["month", category], squeeze=True).count()['__url'].unstack()
        count = count.fillna(0)

        # plot and save
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
