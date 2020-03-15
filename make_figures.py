"""
Utility functions to generate plotly figures from dataframe. Called in app.py
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import plotly.io as pio

pio.templates.default = "plotly_white"

FIRST_LINE_HEIGHT = 600

def make_map(df, country_mapping):
    """
    Build figure with map of total number of cases

    Parameters
    ----------
    df: pandas DataFrame
    """
    df['iso'] = [country_mapping[country] for country in df['country_region']]
    fig = px.choropleth(df, locations='iso', color=np.log10(df['value']),
                    hover_data=[df['value'], df['country_region']],
                    color_continuous_scale='Plasma_r')
    fig.update_layout(title='Click on map to select a country',
            coloraxis_colorbar_tickprefix='1.e',
            margin=dict(l=0, r=0),
            height=FIRST_LINE_HEIGHT)
    fig.update_traces(
        hovertemplate='<b>Country</b>:%{customdata[1]}<br><b>Cases</b>:%{customdata[0]}',
        )
    return fig


def make_timeplot(df_measure, df_prediction):
    """
    Build figure showing evolution of number of cases vs. time for all countries.
    The visibility of traces is set to 0 so that the interactive app will
    toggle the visibility.

    Parameters
    ----------
    df_measure: pandas DataFrame
        DataFrame of measured cases, created by :func:`data_input.get_data`, of wide format.

    df_prediction: pandas DataFrame
        DataFrame of predictions, with similar structure as df_measure
    """
    # mode = 'confirmed'
    mode = 'active'
    df_measure_confirmed = df_measure[mode]
    colors = px.colors.qualitative.Dark24
    n_colors = len(colors)
    fig = go.Figure()
    for i, country in enumerate(df_measure_confirmed.columns):
        fig.add_trace(go.Scatter(x=df_measure_confirmed.index, 
                                 y=df_measure_confirmed[country],
                                 name=country[1], mode='markers+lines',
                                 marker_color=colors[i%n_colors],
                                 line_color=colors[i%n_colors],
                                 visible=False))
    for i, country in enumerate(df_prediction.columns):
        fig.add_trace(go.Scatter(x=df_prediction.index, 
                                 y=df_prediction[country],
                                 name='+' + country[1], mode='lines',
                                 line_dash='dash',
                                 line_color=colors[i%n_colors],
                                 showlegend=False,
                                 visible=False))

    fig.update_layout(title='',
            xaxis=dict(rangeslider_visible=True,
                range=('2020-02-15', '2020-03-13'))) #TODO use a variable for max date
    fig.update_layout(
        updatemenus=[
        dict(
            type = "buttons",
            direction = "left",
            buttons=list([
                dict(
                    args=[{"visible": [False,]*len(df_measure_confirmed.columns)}],
                    label="Reset",
                    method="update",
                ),
                dict(
                    args=["yaxis", {'type':'log'}],
                    label="log",
                    method="relayout",
                ),
                dict(
                    args=["yaxis", {'type':'linear'}],
                    label="lin",
                    method="relayout",
                ),

            ]),
            pad={"r": 10, "t": 10, "b":5},
            showactive=True,
            x=0.05,
            xanchor="left",
            y=1.35,
            yanchor="top",
            font_color='black',
        ),
    ],
    height=.9*FIRST_LINE_HEIGHT,
)

    return fig



