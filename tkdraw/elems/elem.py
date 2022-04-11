class Elem:
    def __init__(self):
        self.handles = []

    def move_handle(self, i, x, y):
        self.handles[i] = (x, y)

    def nearest_point(self, x, y):
        raise NotImplementedError
