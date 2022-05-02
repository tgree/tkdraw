from .vec import Vec
from .line_segment import LineSegment


class Rect:
    def __init__(self, p0, p1):
        self.p0     = p0
        self.p1     = p1

        l = min(p0.x, p1.x)
        r = max(p0.x, p1.x)
        t = min(p0.y, p1.y)
        b = max(p0.y, p1.y)

        self.width  = r - l
        self.height = b - t

        self.nw = Vec(l, t)
        self.ne = Vec(r, t)
        self.se = Vec(r, b)
        self.sw = Vec(l, b)

        self.segments = [
            LineSegment(self.nw, self.ne),
            LineSegment(self.ne, self.se),
            LineSegment(self.se, self.sw),
            LineSegment(self.sw, self.nw),
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

    @staticmethod
    def origin(w, h):
        '''
        Returns a rectangle of width w and height h centered at the origin.
        '''
        return Rect(Vec(-w/2, -h/2), Vec(w/2, h/2))

    @staticmethod
    def square(l):
        '''
        Returns a square with dimension l centered at the origin.
        '''
        return Rect.origin(l, l)

    @staticmethod
    def from_vec(v):
        '''
        Returns a (0, 0) - (v.x, v.y) rectangle.
        '''
        return Rect(Vec(0, 0), v)

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

    def overlaps_point(self, P):
        '''
        Returns True if the point P is contained within the rectangle, False
        otherwise.
        '''
        return self.nw.x <= P.x <= self.se.x and self.nw.y <= P.y <= self.se.y

    def overlaps_rect(self, R):
        '''
        Returns True if the rectangles overlap, even if just at a point.  We
        don't overlap if one rectangle is above or to the left of the other.
        '''
        if self.ne.x < R.nw.x or R.ne.x < self.nw.x:
            return False
        if self.sw.y < R.nw.y or R.sw.y < self.nw.y:
            return False
        return True

    def nearest_point(self, P):
        '''
        Returns the nearest contained within or on the rectangle bounds to the
        point P.
        '''
        if P.x < self.nw.x:
            return self.segments[3].nearest_point(P)
        if P.x > self.ne.x:
            return self.segments[1].nearest_point(P)
        if P.y < self.nw.y:
            return self.segments[0].nearest_point(P)
        if P.y > self.se.y:
            return self.segments[2].nearest_point(P)
        return P
