from .vec import Vec
from .line_segment import LineSegment


class Rect:
    def __init__(self, p0, p1):
        self.p0     = p0
        self.p1     = p1
        self.width  = abs(p1.x - p0.x)
        self.height = abs(p1.y - p0.y)

        p2 = Vec(p0.x, p1.y)
        p3 = Vec(p1.x, p0.y)
        self.segments = [
            LineSegment(p0, p2),
            LineSegment(p2, p1),
            LineSegment(p1, p3),
            LineSegment(p3, p0),
            ]

    def __add__(self, other):
        return Rect(self.p0 + other, self.p1 + other)

    def __sub__(self, other):
        return Rect(self.p0 - other, self.p1 - other)

    @staticmethod
    def zero():
        '''
        Returns a (0, 0) - (0, 0) rectangle.
        '''
        return Rect(Vec(0, 0), Vec(0, 0))

    def line_intersection_ts(self, L):
        '''
        Returns all t values for the line L that intersect any edge segment of
        the rectangle.  If the line intersects one of the rectangle vertices,
        then that t value will be repeated in the returned list.
        '''
        ts = []
        for s in self.segments:
            t, u = L.intersection_t(s.line)
            if u is not None and 0 <= u <= 1:
                ts.append(t)
        return ts

    def overlaps_segment(self, S):
        '''
        Returns True if this rectangle either partially or fully overlaps the
        segment S.  Returns False otherwise.
        '''
        ts = self.line_intersection_ts(S.line)
        if not ts:
            return False
        return min(ts) <= 1 and max(ts) >= 0
