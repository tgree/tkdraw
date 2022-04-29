from .elem import Elem
from .. import coords
from .. import geom


class LineElem(Elem):
    def __init__(self, tk_elem, p0, p1):
        '''
        Given start and end points, p0 and p1, create a LineElem.
        '''
        super().__init__()

        self.tk_elem = tk_elem
        self.segment = geom.LineSegment(p0, p1)
        self.handles.append(p0)
        self.handles.append(p1)

    def __repr__(self):
        return 'LineElem(%u, %u, %u, %u)' % (
                self.segment.line.p0.x, self.segment.line.p0.y,
                self.segment.line.p1.x, self.segment.line.p1.y)

    def move_line(self, p0, p1):
        self.segment = geom.LineSegment(p0, p1)
        self.handles[0] = p0
        self.handles[1] = p1
        self.tk_elem.move_line(
                coords.gridx_to_canvasx(p0.x),
                coords.gridy_to_canvasy(p0.y),
                coords.grid_to_canvas_delta(self.segment.line.dt.x),
                coords.grid_to_canvas_delta(self.segment.line.dt.y))

    def translate(self, dx, dy):
        d = geom.Vec(dx, dy)
        self.move_line(self.segment.line.p0 + d, self.segment.line.p1 + d)

    def nearest_point(self, P):
        '''
        Returns the nearest point on the line segment to the point P = (x, y).
        '''
        return self.segment.nearest_point(P)

    def overlaps_rect(self, R):
        '''
        Returns True if this line segment partially or fully overlaps the
        rectangle R.  Returns False otherwise.
        '''
        return R.overlaps_segment(self.segment)
