
class Customer():
    def __init__(self, created_at) -> None:
        self.created_at = created_at
        self.orders = []
        self.last_ordered = None
