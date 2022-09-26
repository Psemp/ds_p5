import pandas
import numpy
import plotly.graph_objects as go

from models.group_stats import Group_stats


class Cx_groups():
    def __init__(self, cluster_name: str, dataframe: pandas.DataFrame) -> None:
        self.name = cluster_name
        self.dataframe = dataframe
        self.got_standard_stats = False
        self.got_scaled_stats = False

    def calc_average_var(self, dataframe, target):
        return numpy.average(
                dataframe[dataframe[target].notna()][target]
            )

    def get_standard_stats(self):

        self.standard_stats = Group_stats(
                rating_avg=self.calc_average_var(dataframe=self.dataframe, target="rating_avg"),
                delta_days=self.calc_average_var(dataframe=self.dataframe, target="delta_days"),
                distance_cx_seller=self.calc_average_var(dataframe=self.dataframe, target="distance_cx_seller"),
                recency=self.calc_average_var(dataframe=self.dataframe, target="recency"),
                frequency=self.calc_average_var(dataframe=self.dataframe, target="frequency"),
            )
        self.got_standard_stats = True

    def get_scaled_stats(self):

        self.scaled_stats = Group_stats(
                rating_avg=self.calc_average_var(dataframe=self.dataframe, target="scaled_rating_avg"),
                delta_days=self.calc_average_var(dataframe=self.dataframe, target="scaled_delta_days"),
                distance_cx_seller=self.calc_average_var(
                    dataframe=self.dataframe,
                    target="scaled_distance_cx_seller"
                    ),
                recency=self.calc_average_var(dataframe=self.dataframe, target="scaled_recency"),
                frequency=self.calc_average_var(dataframe=self.dataframe, target="scaled_frequency"),
            )
        self.got_scaled_stats = True

    def get_radar(self):

        if not self.got_scaled_stats:
            self.get_scaled_stats()

        r_values = [
            self.scaled_stats.rating_avg, self.scaled_stats.delta_days, self.scaled_stats.distance_cx_seller,
            self.scaled_stats.recency, self.scaled_stats.frequency
            ]
        thetas = ["rating_avg", "delta_days", "distance_cx_seller", "recency", "frequency"]
        self.trace = go.Scatterpolar(r=r_values, theta=thetas, fill="toself", name=f"radar {self.name}")

        fig = go.Figure(data=self.trace)

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True
                ),
            ),
            showlegend=False
        )

        return fig

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name
