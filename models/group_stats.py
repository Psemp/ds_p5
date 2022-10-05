from collections import namedtuple


fields = ["rating_avg", "delta_days", "distance_cx_seller", "recency", "frequency"]


def create_group_stats(subset):
    Group_stats = namedtuple("Group_stats", field_names=subset)
    return Group_stats
