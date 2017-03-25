import io
import requests

import pandas as pd
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import (
    CategoricalColorMapper, ColumnDataSource,
    Select, Slider, Button, RangeSlider, Range1d,
    HoverTool, Legend
)
from bokeh.models.renderers import GlyphRenderer as Glyph
from bokeh.plotting import figure
# set hieght and width
H = 600
W = 600

# color map palete
palette=[
    '#8dd3c7', '#dfdf93', '#bebada',
    '#fb8072', '#80b1d3', '#fdb462'
]

# read in gapminder data from AWS
url = "https://s3-us-west-2.amazonaws.com/gap-minder-flat-files/data.csv"
data = requests.get(url).content
data = data.decode("utf-8")
data = io.StringIO(data)
df = pd.read_csv(data, index_col=0)

# define widgets for customizing plot
year_slider = Slider(title='Year', start=1964, end=2013, step=1, value=1964, width=W + 300)

x_select = Select(title='X Value', options=['Life Expectancy', 'Population', 'Fertility'], value='Fertility')
xs_select = Select(title='Scale', options=['Linear', 'Log'], value='Linear')

y_select = Select(title='Y Value', options=['Life Expectancy', 'Population', 'Fertility'], value='Population')
ys_select = Select(title='Scale', options=['Linear', 'Log'], value='Linear')

s_select = Select(title='Size Value', options=['Life Expectancy', 'Population', 'Fertility'],
                  value='Population')
sr_select = Select(title='Size Scale', options=['Linear', 'Log', 'Square'], value='Linear')
sr_slider = RangeSlider(title='Scale Range', start=1, end=40, step=1, range=(10, 20))

back_button = Button(label='⏮', width=55, name='Play Through Years')
reverse_button = Button(label='◀', width=55)
stop_button = Button(label='⏹', width=55)
play_button = Button(label='▶', width=55)
forward_button = Button(label='⏭', width=55)


# scale function for size values
def scale(value):
    vmax = df[s_select.value].max()
    vmin = df[s_select.value].min()
    smax = sr_slider.range[1]
    smin = sr_slider.range[0]
    if sr_select.value == 'Log':
        vmax = np.log(vmax)
        vmin = np.log(vmin)
        value = np.log(value)
    elif sr_select.value == 'Square':
        vmax = np.square(vmax)
        vmin = np.square(vmin)
        value = np.square(value)
    m = (smax - smin) / (vmax - vmin)
    b = smin - m * vmin
    return(value * m + b)


def create_plot():
    # refine df by year and create initial column data source
    global source
    global hover
    df_year = df.loc[year_slider.value]

    source = ColumnDataSource({
        'x': df_year[x_select.value],
        'y': df_year[y_select.value],
        'size': scale(df_year[s_select.value]),
        'country': df_year['Country'],
        'region': df_year['Group']
    })

    # make a hover tool
    hover = HoverTool(
        tooltips=[
            ('Country', '@country'),
            (x_select.value, '@x'),
            (y_select.value, '@y'),
            (s_select.value, '@size')
        ])

    # color mapper
    cmap = CategoricalColorMapper(factors=list(df['Group'].unique()),
                                  palette=palette)

    x_axis_type = xs_select.value.lower()
    y_axis_type = ys_select.value.lower()

    # range values
    xmax = df[x_select.value].max()
    xmax += 0.1 * xmax
    xmin = 0 if x_axis_type == 'linear' else df[x_select.value].min()
    ymax = df[y_select.value].max()
    ymax += 0.1 * ymax
    ymin = 0 if y_axis_type == 'linear' else df[y_select.value].min()

    x_range = (xmin, xmax)
    y_range = (ymin, ymax)

    # initialize figure
    fig = figure(plot_height=H,
                 plot_width=W,
                 x_range=x_range,
                 y_range=y_range,
                 x_axis_type=x_axis_type,
                 y_axis_type=y_axis_type)

    fig.add_tools(hover)

    fig.title.text = '{} vs. {} {}'.format(
        x_select.value, y_select.value, year_slider.value
    )
    fig.xaxis.axis_label = x_select.value
    fig.yaxis.axis_label = y_select.value

    # plot initial data
    fig.circle(x='x', y='y',
               size='size',
               color={'field': 'region',
                      'transform': cmap},
               alpha=0.7,
               source=source)

    return fig


def create_legend_fig():
    leg = figure(height=H,
                 width=300,
                 x_axis_type=None,
                 y_axis_type=None,
                 min_border=0,
                 outline_line_color='#FFFFFF')

    leg.toolbar_location = None

    for region, color in zip(df['Group'].unique(), palette):
        leg.circle(0, 0, color=color, alpha=0.7, legend=region)

    leg.legend.location = 'top_left'

    def invisify(r):
        r.visible = False
        return r

    leg.renderers = [(invisify(r) if type(r) == Glyph else r)
                     for r in leg.renderers]
    return leg



    # still needs more see email list!!!




def update(attr, old, new):
    # update plot with new values
    df_year = df.loc[year_slider.value].copy()

    source.data = {
        'x': df_year[x_select.value],
        'y': df_year[y_select.value],
        'size': scale(df_year[s_select.value]),
        'country': df_year['Country'],
        'region': df_year['Group']
    }

    fig.title.text = '{} vs. {}\n{}'.format(
        x_select.value, y_select.value, year_slider.value
    )

def update_plot(att, old, new):
    global fig
    fig = create_plot()
    layout.children[0].children[1] = fig


def play():
    global play_direction
    play_direction = 1
    curdoc().add_periodic_callback(itter, 250)


def reverse():
    global play_direction
    play_direction = -1
    curdoc().add_periodic_callback(itter, 250)


def itter():
    global play_direction
    if play_direction == 1:
        target = year_slider.end
    else:
        target = year_slider.start
    if year_slider.value != target:
        year_slider.value += play_direction * year_slider.step
    else:
        del play_direction
        curdoc().remove_periodic_callback(itter)


def stop():
    try:
        curdoc().remove_periodic_callback(itter)
    except Exception:
        pass


def back():
    year_slider.value = year_slider.start


def forward():
    year_slider.value = year_slider.end


fig = create_plot()
legend = create_legend_fig()
# create dashboard layout
layout = column(
    row(
        column(x_select,
               xs_select,
               y_select,
               ys_select,
               s_select,
               sr_slider,
               sr_select,
               row(back_button,
                   reverse_button,
                   stop_button,
                   play_button,
                   forward_button)),
        fig, legend),

    year_slider
)


x_select.on_change('value', update_plot)
xs_select.on_change('value', update_plot)
y_select.on_change('value', update_plot)
ys_select.on_change('value', update_plot)
s_select.on_change('value', update_plot)
sr_select.on_change('value', update)
sr_slider.on_change('range', update)
year_slider.on_change('value', update)
play_button.on_click(play)
reverse_button.on_click(reverse)
stop_button.on_click(stop)
back_button.on_click(back)
forward_button.on_click(forward)


curdoc().add_root(layout)
