class Line:
    '''
    Implements a line in 2-D space using a parametric equation of the form:

        p(t) = p0 + (p1 - p0)*t

    p0 and p1 should both be Vec objects.  This has the following properties:

        p(0) = p0
        p(1) = p1

    And therefore if the p0 and p1 represent a line segment l contained on the
    line L, then all points in l fall in the region 0 <= t <= 1.
    '''
    def __init__(self, p0, p1):
        self.p0  = p0
        self.p1  = p1
        self.dt  = p1 - p0
        self.dt2 = self.dt.norm_squared()

    def __repr__(self):
        return 'Line((%s, %s), (%s, %s))' % (
                self.p0.x, self.p0.y, self.p1.x, self.p1.y)

    def __eq__(self, other):
        return ((self.p0 == other.p0 and self.p1 == other.p1) or
                (self.p0 == other.p1 and self.p1 == other.p0))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __call__(self, t):
        return self.p0 + self.dt * t

    def nearest_point_t(self, p):
        '''
        Returns the t value of the nearest point on the line to the target
        point p.
        '''
        vp = p - self.p0
        return vp.dot(self.dt) / self.dt2

    def nearest_point(self, p):
        '''
        Returns the nearest point on the line to the target point p.
        '''
        return self(self.nearest_point_t(p))

    def intersection_t(self, l):
        '''
        Returns a tuple (t1, t2) for the intersection with the line l.  The t1
        value is for our line and the t2 value is for l.  Both should evaluate
        to the same point within the floating point error.  For the case where
        the lines are collinear, even if they are right on top of each other, we
        return (None, None).
        '''
        # The determinant of the matrix also happens (unsurprisingly) to be the
        # exact condition to check for collinearity.
        det = self.dt.x * l.dt.y - l.dt.x * self.dt.y
        if det == 0:
            return None, None

        d = l.p0 - self.p0
        t = (   l.dt.y * d.x -    l.dt.x * d.y) / det
        u = (self.dt.y * d.x - self.dt.x * d.y) / det
        return t, u

    def intersection(self, l):
        '''
        Returns the point of intersection with the line l.  If the two vectors
        are collinear and do not intersect, we return None.
        '''
        t, _u = self.intersection_t(l)
        return self(t)
