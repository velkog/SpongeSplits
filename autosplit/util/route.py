from config import get_route


class Route():
    def __init__(self):
        self.route = get_route()

    def next_split(self):
        return self.route[0]

    def split(self):
        self.route.pop()
