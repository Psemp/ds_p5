import pandas
from sklearn.preprocessing import MinMaxScaler

from scripts.model_helpers import get_radar, calc_average_var
from models.group_stats import create_group_stats


class Cx_groups_post_pca():
    def __init__(self, dataframe: pandas.DataFrame, k_group: int, cluster_col: str) -> None:
        self.name = None
        self.k_group = k_group
        self.dataframe_full = dataframe
        self.cluster_col = cluster_col
        self.dataframe = dataframe[dataframe[self.cluster_col] == self.k_group]
        self.got_standard_stats = False
        self.subset = [
                "time_impact", "general_involvment", "overall_discontentment",
                "overall_satisfaction", "value_and_volume",
            ]
        self.scaled_subset = [f"scaled_{col}" for col in self.subset]
        self.got_standard_stats = False
        self.got_scaled_stats = False
        self.scaled = False

    def get_standard_stats(self):
        Group_stats = create_group_stats(subset=self.subset)
        self.standard_stats = Group_stats(
                time_impact=calc_average_var(dataframe=self.dataframe, target=self.subset[0]),
                general_involvment=calc_average_var(
                    dataframe=self.dataframe,
                    target=self.subset[1]
                    ),
                overall_discontentment=calc_average_var(
                    dataframe=self.dataframe,
                    target=self.subset[2]
                    ),
                overall_satisfaction=calc_average_var(
                    dataframe=self.dataframe,
                    target=self.subset[3]
                    ),
                value_and_volume=calc_average_var(dataframe=self.dataframe, target=self.subset[4]),
            )
        self.got_standard_stats = True

    def scale_df(self):
        mmx = MinMaxScaler(feature_range=(0, 10))
        self.dataframe_mmx_full = self.dataframe_full.copy()
        self.dataframe_mmx_full[self.scaled_subset] = mmx.fit_transform(self.dataframe_full[self.subset].to_numpy())
        self.dataframe_mmx = self.dataframe_mmx_full[self.dataframe_mmx_full[self.cluster_col] == self.k_group]
        self.scaled = True

    def get_scaled_stats(self):
        if not self.scaled:
            self.scale_df()
            self.scaled = True

        Group_stats = create_group_stats(subset=self.scaled_subset)
        self.scaled_stats = Group_stats(
                scaled_time_impact=calc_average_var(
                    dataframe=self.dataframe_mmx,
                    target=self.scaled_subset[0]
                    ),
                scaled_general_involvment=calc_average_var(
                    dataframe=self.dataframe_mmx,
                    target=self.scaled_subset[1]
                    ),
                scaled_overall_discontentment=calc_average_var(
                    dataframe=self.dataframe_mmx,
                    target=self.scaled_subset[2]
                    ),
                scaled_overall_satisfaction=calc_average_var(
                    dataframe=self.dataframe_mmx,
                    target=self.scaled_subset[3]
                    ),
                scaled_value_and_volume=calc_average_var(
                    dataframe=self.dataframe_mmx,
                    target=self.scaled_subset[4]
                    ),
            )
        self.got_scaled_stats = True

    def store_radar(self):

        if not self.got_scaled_stats:
            self.get_scaled_stats()

        r_values = [stat for stat in self.scaled_stats]
        thetas = self.scaled_subset

        if self.name is None:
            fig_name = self.k_group
        else:
            fig_name = self.name
        radar = get_radar(stats=r_values, subset=thetas, name=fig_name)
        self.trace = radar[0]
        return radar[1]

    def __str__(self) -> str:
        if self.name is None:
            return self.k_group
        else:
            return self.name

    def __repr__(self) -> str:
        if self.name is None:
            return self.k_group
        else:
            return self.name
