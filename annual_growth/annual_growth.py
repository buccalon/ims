# crescimento dos acervos

import pandas as pd

from bokeh.io import output_file, show
from bokeh.models import (
    ColumnDataSource,
    DatetimeTickFormatter,
    NumeralTickFormatter,
    CustomJS,
)
from bokeh.models.tools import HoverTool
from bokeh.plotting import figure
from bokeh.layouts import column

output_file("annual_growth.html")


# load data
csv = pd.read_csv("./annual_growth.csv", parse_dates=["year"])
source = ColumnDataSource(csv)
years_list = csv["year"].dt.year.tolist()

# ----------------------

code1 = "source.set('collections', cb_data['index']);"
code2 = "source.set('items', cb_data['index']);"
callback = CustomJS(args={"source": source, "source": source}, code=code1 + code2)

# create plot
p1 = figure(
    plot_width=1280,
    plot_height=480,
    # title=f"Total de itens ({years_list[0]} - {years_list[-1]})",
    toolbar_location=None,
    x_axis_type="datetime",
)

# plot data
c1 = p1.vbar(
    x="year",
    top="items",
    source=source,
    color="orange",
    hover_color="tomato",
    width=25000000000,
)


TOOLTIPS_P1 = """
    <div>
        <div>
            <span style="font-size: 1.4em; color: #555;">@year{%Y}</span>
        </div>
        <div>
            <span style="font-size: 1.8em; font-weight: bold;">@items{0.0a} itens</span>
        </div>
    </div>
"""

# tooltips


# y-axis label
p1.yaxis.axis_label = "Total de itens"
p1.yaxis[0].formatter = NumeralTickFormatter(format="0.0 a")

# format settings
p1.xgrid.grid_line_color = None
p1.toolbar.active_drag = None
p1.y_range.start = 0
p1.background_fill_color = "lightgrey"
p1.background_fill_alpha = 0.2
p1.title.text_font_size = "1.8em"
p1.title.text_font = "arial"
p1.title.align = "center"
p1.yaxis.axis_label_standoff = 15
p1.yaxis.axis_label_text_font_size = "1.2em"
p1.min_border = 20
p1.yaxis.minor_tick_line_color = None


# ----------------------

TOOLTIPS_P2 = """
    <div>
        <div>
            <span style="font-size: 1.4em; color: #555;">@year{%Y}</span>
        </div>
        <div>
            <span style="font-size: 1.8em; font-weight: bold;">@collections coleções</span>
        </div>
    </div>
"""

# create plot
p2 = figure(
    plot_width=1280,
    plot_height=300,
    title=f"Acervo IMS ({years_list[0]} - {years_list[-1]})",
    toolbar_location=None,
    x_range=p1.x_range,
    x_axis_type="datetime",
)

# plot data
p2.line(
    x="year",
    y="collections",
    line_dash="4 4",
    source=source,
    color="lightgray",
    line_width=3,
)
c2 = p2.circle(
    x="year",
    y="collections",
    source=source,
    color="orange",
    hover_color="tomato",
    fill_color="orange",
    size=18,
)

p1_hover = HoverTool(
    callback=callback,
    renderers=[c1, c2],
    tooltips=TOOLTIPS_P1,
    point_policy="follow_mouse",
    formatters={"@year": "datetime", "@items": "numeral"},
    mode="vline",
    show_arrow=False,
    line_policy="nearest",
)
p1.add_tools(p1_hover)

# tooltips
p2_hover = HoverTool(
    callback=callback,
    renderers=[c1, c2],
    tooltips=TOOLTIPS_P2,
    point_policy="follow_mouse",
    formatters={"@year": "datetime",},
    mode="vline",
    show_arrow=False,
    line_policy="nearest",
)
p2.add_tools(p2_hover)


# y-axis label
p2.yaxis.axis_label = "Total de coleções"

# format settings
p2.xgrid.grid_line_color = None
p2.toolbar.active_drag = None
p2.y_range.start = 0
p2.background_fill_color = "lightgrey"
p2.background_fill_alpha = 0.2
p2.title.text_font_size = "2.4em"
p2.title.text_font = "arial"
p2.title.text_line_height = 2
p2.title.align = "center"
p2.title.vertical_align = "middle"
p2.yaxis.minor_tick_line_color = None

p2.yaxis.axis_label_standoff = 30
p2.yaxis.axis_label_text_font_size = "1.2em"
p2.min_border = 20


# ----------------------

show(column(p2, p1, sizing_mode="stretch_both"))
