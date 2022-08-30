import pandas


def get_order_details(cx_uid: int, uid_col: str, from_frame: pandas.DataFrame) -> dict:
    order_details = {}
    order_details["order_list"] = from_frame[from_frame[uid_col] == cx_uid]["order_id"].values
    order_details["total_spent"] = from_frame[from_frame[uid_col] == cx_uid]["sum_total"].sum()
    return order_details


def get_min_max_dt(order_list: list, from_frame: pandas.DataFrame, dt_col: str) -> dict:
    order_dict = dict.fromkeys(order_list)
    for order_id in order_dict:
        order_dict[order_id] = from_frame[from_frame["order_id"] == order_id][dt_col].values[0]

    datelist = list(order_dict.values())

    min_max_dt = {
        "min": pandas.to_datetime(min(datelist)),
        "max": pandas.to_datetime(max(datelist))
    }

    return min_max_dt
