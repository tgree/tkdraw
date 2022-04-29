from .line import Line


class LineSegment:
    def __init__(self, p0, p1):
        self.line = Line(p0, p1)

    def __repr__(self):
        return 'LineSegment((%s, %s), (%s, %s))' % (
                self.line.p0.x, self.line.p0.y,
                self.line.p1.x, self.line.p1.y,
                )

    def __eq__(self, other):
        return self.line == other.line

    def __ne__(self, other):
        return self.line != other.line

    def __call__(self, t):
        t = 0 if t < 0 else 1 if t > 1 else t
        return self.line(t)

    def nearest_point_t(self, p):
        t = self.line.nearest_point_t(p)
        t = 0 if t < 0 else 1 if t > 1 else t
        return t

    def nearest_point(self, p):
        return self.line(self.nearest_point_t(p))

    def intersection_t(self, s):
        t, u = self.line.intersection_t(s.line)
        if t is None or u is None:
            return None, None
        if 0 <= t <= 1 and 0 <= u <= 1:
            return t, u
        return None, None

    def shortest_connecting_segment(self, s):
        '''
        Given another line segment, s, find the shortest line segment that
        would connect a point on us to a point on s.
        '''
        if (not self.line.dt.is_collinear(s.line.dt) or
                not self.line.dt.is_collinear(s.line.p0 - self.line.p0)):
            # If they intersect, we return a LineSegment connecting the "two"
            # intersection points, which may or may not both be exactly the same
            # due to floating-point error.
            t, u = self.intersection_t(s)
            if t is not None:
                p0 = self(t)
                p1 = s(u)
                return LineSegment(p0, p1)

            # Not collinear and they don't intersect.  Do projections and find
            # the shortest one.
            ls = [LineSegment(self.line.p0, s.nearest_point(self.line.p0)),
                  LineSegment(self.line.p1, s.nearest_point(self.line.p1)),
                  LineSegment(s.line.p0, self.nearest_point(s.line.p0)),
                  LineSegment(s.line.p1, self.nearest_point(s.line.p1)),
                  ]
        else:
            # Both line segments lie upon the same line.
            raise Exception('Same line not handled yet.')

        best = ls[0]
        for i in range(1, len(ls)):
            if ls[i].line.dt2 < best.line.dt2:
                best = ls[i]

        return best
