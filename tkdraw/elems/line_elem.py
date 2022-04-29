import numpy as np

from .elem import Elem
from .. import coords
from .. import geom


class LineElem(Elem):
    def __init__(self, tk_elem, x, y, w, h):
        super().__init__()

        self.tk_elem = tk_elem
        self.handles.append((x, y))
        self.handles.append((x + w, y + h))

    def __repr__(self):
        return 'LineElem(%u, %u, w=%u, h=%u)' % (
                self.handles[0][0], self.handles[0][1],
                self.handles[1][0] - self.handles[0][0],
                self.handles[1][1] - self.handles[0][1])

    def move_line(self, x, y, w, h):
        self.handles[0] = (x, y)
        self.handles[1] = (x + w, y + h)
        self.tk_elem.move_line(coords.gridx_to_canvasx(x),
                               coords.gridy_to_canvasy(y),
                               coords.grid_to_canvas_delta(w),
                               coords.grid_to_canvas_delta(h))

    def nudge(self, dx, dy):
        x = self.handles[0][0] + dx
        y = self.handles[0][1] + dy
        w = self.handles[1][0] - self.handles[0][0]
        h = self.handles[1][1] - self.handles[0][1]
        self.move_line(x, y, w, h)

    def nearest_point(self, x, y):
        '''
        Returns the nearest point on the line segment to the point P = (x, y).
        We generate the equation of the line:

               v = (h1 - h0)
            L(t) = h0 + t*v

        So that L(0) = h0 and L(1) = h1.

        The dot product of two vectors is defined as:

            a . b = |a| |b| cos(theta)
                  = a.x * b.x + a.y * b.y

        Take the dot product of vp = (P - h0) with v to get the length along
        the vector v where the point projects:

            vp . v = |vp| |v| cos(theta)
                   = |v| * l
                 l = |vp| cos(theta) = (vp . v) / |v|

        The projection point p is l times the unit vector along v:

            p = h0 + (v / |v|) * l
              = h0 + [(vp . v) / (|v|**2)] * v
              = L((vp . v) / (|v|**2))
              = L(t')

        Where:
            t' = (vp . v) / (|v|**2)
               = (vp . v) / (v . v)

        The range of points contained on the line segment are constrained to
        the range for t = 0..1, so if we clamp t' to 0..1 we will have found
        the closest point.
        '''
        h0 = np.array(self.handles[0])
        h1 = np.array(self.handles[1])
        P  = np.array((x, y))
        vp = P - h0
        v  = h1 - h0
        t  = np.dot(vp, v) / np.dot(v, v)
        t  = 0 if t < 0 else 1 if t > 1 else t
        p  = h0 + t * v
        return p[0], p[1]

    def overlaps_rect(self, R):
        '''
        Returns True if this line segment partially or fully overlaps the
        rectangle R.  Returns False otherwise.
        '''
        S = geom.LineSegment(geom.Vec(self.handles[0][0], self.handles[0][1]),
                             geom.Vec(self.handles[1][0], self.handles[1][1]))
        return R.overlaps_segment(S)
