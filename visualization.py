from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Legend
from bokeh.layouts import layout
from bokeh.io import show
import pandas as pd

class RealTimeVisualizer:
    def __init__(self, lot_ids):
        self.sources = {lot: ColumnDataSource(data=dict(ts=[], price1=[], price2=[], price3=[], occupancy=[], queue=[])) for lot in lot_ids}
        self.fig = figure(title="Real-Time Parking Lot Pricing", x_axis_type='datetime', width=1000, height=600)
        self.renderers = {}
        colors = ['blue', 'green', 'red', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'magenta', 'navy', 'teal', 'gold']
        for i, lot in enumerate(lot_ids):
            color = colors[i % len(colors)]
            r1 = self.fig.line('ts', 'price1', source=self.sources[lot], color=color, legend_label=f"{lot} Model1", line_dash='solid')
            r2 = self.fig.line('ts', 'price2', source=self.sources[lot], color=color, legend_label=f"{lot} Model2", line_dash='dashed')
            r3 = self.fig.line('ts', 'price3', source=self.sources[lot], color=color, legend_label=f"{lot} Model3", line_dash='dotdash')
            self.fig.line('ts', 'occupancy', source=self.sources[lot], color=color, legend_label=f"{lot} Occupancy", line_dash='dotted', alpha=0.3)
            self.fig.line('ts', 'queue', source=self.sources[lot], color=color, legend_label=f"{lot} Queue", line_dash='dotted', alpha=0.6)
            self.renderers[lot] = (r1, r2, r3)
        self.fig.legend.click_policy = "hide"
        self.layout = layout([[self.fig]])

    def update(self, batch):
        for row in batch:
            lot = row['LotID']
            src = self.sources[lot]
            new_data = dict(
                ts=[row['Timestamp']],
                price1=[row['Price1']],
                price2=[row['Price2']],
                price3=[row['Price3']],
                occupancy=[row['Occupancy']],
                queue=[row['QueueLength']]
            )
            src.stream(new_data, rollover=200)

    def show(self):
        show(self.layout) 