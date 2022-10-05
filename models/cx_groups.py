import pandas

from models.group_stats import create_group_stats
from scripts.model_helpers import get_radar, calc_average_var


class Cx_groups():
    def __init__(self, cluster_name: str, dataframe: pandas.DataFrame) -> None:
        self.name = cluster_name
        self.dataframe = dataframe
        self.got_standard_stats = False
        self.got_scaled_stats = False
        self.subset = ["rating_avg", "delta_days", "distance_cx_seller", "recency", "frequency"]
        self.scaled_subset = [f"scaled_{col}" for col in self.subset]

    def get_standard_stats(self):
        Group_stats = create_group_stats(subset=self.subset)
        self.standard_stats = Group_stats(
                rating_avg=calc_average_var(dataframe=self.dataframe, target="rating_avg"),
                delta_days=calc_average_var(dataframe=self.dataframe, target="delta_days"),
                distance_cx_seller=calc_average_var(dataframe=self.dataframe, target="distance_cx_seller"),
                recency=calc_average_var(dataframe=self.dataframe, target="recency"),
                frequency=calc_average_var(dataframe=self.dataframe, target="frequency"),
            )
        self.got_standard_stats = True

    def get_scaled_stats(self):
        Group_stats = create_group_stats(subset=self.scaled_subset)
        self.scaled_stats = Group_stats(
                scaled_rating_avg=calc_average_var(dataframe=self.dataframe, target="scaled_rating_avg"),
                scaled_delta_days=calc_average_var(dataframe=self.dataframe, target="scaled_delta_days"),
                scaled_distance_cx_seller=calc_average_var(
                    dataframe=self.dataframe,
                    target="scaled_distance_cx_seller"
                    ),
                scaled_recency=calc_average_var(dataframe=self.dataframe, target="scaled_recency"),
                scaled_frequency=calc_average_var(dataframe=self.dataframe, target="scaled_frequency"),
            )
        self.got_scaled_stats = True

    def store_radar(self):

        if not self.got_scaled_stats:
            self.get_scaled_stats()

        r_values = [stat for stat in self.scaled_stats]
        thetas = self.scaled_subset
        radar = get_radar(stats=r_values, subset=thetas, name=self.name)
        self.trace = radar[0]
        return radar[1]

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name
