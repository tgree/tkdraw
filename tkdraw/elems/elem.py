class Elem:
    def __init__(self):
        self.handles = []

    def translate(self, dv):
        raise NotImplementedError

    def is_handle_interactive(self, index):
        raise NotImplementedError

    def drag_handle(self, index, mp):
        raise NotImplementedError

    def nearest_point(self, P):
        raise NotImplementedError

    def overlaps_rect(self, R):
        raise NotImplementedError

    def add_inspector(self, workspace):
        raise NotImplementedError
