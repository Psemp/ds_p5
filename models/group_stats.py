from collections import namedtuple


fields = ["rating_avg", "delta_days", "distance_cx_seller", "recency", "frequency"]
Group_stats = namedtuple("Group_stats", field_names=fields)
