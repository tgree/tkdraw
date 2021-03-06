from .elem import Elem
from .. import coords
from .. import geom


class LineElem(Elem):
    NN_SLOP = 4

    def __init__(self, workspace, p0, p1):
        '''
        Given start and end points, p0 and p1, create a LineElem.
        '''
        super().__init__()

        self.workspace = workspace
        self.tk_elem   = workspace.add_line(p0, p1)
        self.segment   = geom.LineSegment(p0, p1)
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
        self.workspace.notify_handles_changed(self, [0, 1])

    def translate(self, dv):
        '''
        Translates the line by the delta-vector dv.
        '''
        self.move_line(self.segment.line.p0 + dv, self.segment.line.p1 + dv)

    def is_handle_interactive(self, _index):
        '''
        Both line handles are interactive and used to drag the endpoints around.
        '''
        return True

    def drag_handle(self, index, mp):
        '''
        Drags the handle index to the specified MousePoint.
        '''
        self.handles[index] = mp
        self.move_line(self.handles[0], self.handles[1])

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

    def add_inspector(self, _workspace):
        return None
