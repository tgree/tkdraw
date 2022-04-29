class Elem:
    def __init__(self):
        self.handles = []

    def translate(self, dx, dy):
        raise NotImplementedError

    def nearest_point(self, P):
        raise NotImplementedError
