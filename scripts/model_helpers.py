import plotly.graph_objects as go
import numpy


def get_radar(stats: list, subset: list, name: str = None):

    r_values = [stat for stat in stats]
    thetas = subset
    trace = go.Scatterpolar(r=r_values, theta=thetas, fill="toself", name=f"radar {name}")

    fig = go.Figure(data=trace)

    fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True
                ),
            ),
            showlegend=False
        )

    return trace, fig


def calc_average_var(dataframe, target):
    return numpy.average(
            dataframe[dataframe[target].notna()][target]
        )
