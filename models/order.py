
class Order():

    def __init__(self, order_id, date_ordered, sum_total) -> None:

        self.order_id = order_id
        self.date_ordered = date_ordered
        self.sum_total = sum_total

    def shrink(self):
        ...

    def __str__(self) -> str:
        return self.order_id

    def __repr__(self) -> str:
        return self.order_id
