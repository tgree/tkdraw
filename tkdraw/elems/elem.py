class Elem:
    def __init__(self):
        self.handles = []

    def nudge(self, dx, dy):
        raise NotImplementedError

    def nearest_point(self, x, y):
        raise NotImplementedError
