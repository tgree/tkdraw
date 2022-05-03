import tkinter.font

from .elem import Elem
from ..inspectors import TextEntryInspector
from .. import coords
from .. import geom


class TextElem(Elem):
    NN_SLOP = 0

    def __init__(self, workspace, p0, text):
        '''
        Given a point and text, create a TextElem centered on that point.
        '''
        super().__init__()

        self.tk_elem = workspace.add_text(p0, text=text, anchor='c',
                                          justify='center')
        self.tk_font = tkinter.font.nametofont(self.tk_elem.cget('font'))

        self.workspace   = workspace
        self.p0          = p0
        self.text        = None
        self.text_width  = None
        self.text_height = None
        self.dv          = None
        self.brect       = None
        self.handles     = [None, None, None, None]

        self.set_text(text)
        self.move_text(p0)

    def _update_handles(self):
        self.brect      = geom.Rect(self.p0 - self.dv, self.p0 + self.dv)
        self.handles[0] = self.brect.nw
        self.handles[1] = self.brect.ne
        self.handles[2] = self.brect.se
        self.handles[3] = self.brect.sw
        self.workspace.notify_handles_changed(self, [0, 1, 2, 3])

    def set_text(self, text):
        lines = (text + '\n').splitlines()
        w     = max(self.tk_font.measure(l) for l in lines)
        h     = self.tk_font.metrics('linespace') * len(lines)

        self.text        = text
        self.text_width  = coords.canvas_to_grid_delta(w)
        self.text_height = coords.canvas_to_grid_delta(h)
        self.dv          = geom.Vec(self.text_width / 2, self.text_height / 2)
        self.tk_elem.configure(text=text)

        self._update_handles()

    def __repr__(self):
        return 'TextElem(%u, %u)' % (self.p0.x, self.p0.y)

    def move_text(self, p0):
        self.p0 = p0
        self.tk_elem.move_to(coords.gridx_to_canvasx(p0.x),
                             coords.gridy_to_canvasy(p0.y))

        self._update_handles()

    def translate(self, dv):
        self.move_text(self.p0 + dv)

    def is_handle_interactive(self, _index):
        return False

    def drag_handle(self, index, mp):
        raise Exception('No interactive handles.')

    def nearest_point(self, P):
        return self.brect.nearest_point(P)

    def overlaps_rect(self, R):
        return self.brect.overlaps_rect(R)

    def add_inspector(self, workspace):
        return TextEntryInspector(workspace, elem=self)
