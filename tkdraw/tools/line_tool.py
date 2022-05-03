from enum import Enum

from .tool import Tool
from ..elems import LineElem
from ..inspectors import CoordinatesInspector
from .. import geom


class State(Enum):
    IDLE         = 0
    DRAG_STARTED = 1


class LineTool(Tool):
    INSPECT_TITLE = 'LINE TOOL'

    def __init__(self, workspace, R, *args, **kwargs):
        super().__init__(workspace, R, *args, **kwargs)
        self.state     = State.IDLE
        self.line_elem = None
        self.icon_line = workspace.tool_canvas.add_line(
                R.p0 + geom.Vec(10, 10), R.p1 - geom.Vec(10, 10))

        self.coordinates_inspector = None

    def _go_idle(self):
        if self.state == State.DRAG_STARTED:
            self.workspace.delete_canvas_elem(self.line_elem.tk_elem)
            self.line_elem = None
            self.state     = State.IDLE

    def handle_app_activated(self):
        assert self.state == State.IDLE

    def handle_app_deactivated(self):
        self._go_idle()

    def handle_tool_selected(self):
        self.icon_border.configure(outline='black')
        assert self.state == State.IDLE

        ic = self.workspace.inspect_canvas
        self.coordinates_inspector = CoordinatesInspector(ic, 2)

    def handle_tool_deselected(self):
        self.icon_border.configure(outline='#CCCCCC')
        self._go_idle()

    def handle_canvas_entered(self, p):
        self.workspace._root.configure(cursor='tcross')

    def handle_canvas_exited(self):
        self.workspace._root.configure(cursor='arrow')

    def handle_key_pressed(self, e):
        if self.state == State.DRAG_STARTED:
            if e.keysym == 'Escape':
                self._go_idle()

    def handle_mouse_down(self, p):
        assert self.state == State.IDLE
        self.line_elem = LineElem(self.workspace, p, p)
        self.state     = State.DRAG_STARTED
        self.coordinates_inspector.set_coord(0, p)
        self.coordinates_inspector.set_coord(1, p)

    def handle_mouse_up(self, p):
        self.coordinates_inspector.set_coord(0, p)
        self.coordinates_inspector.set_coord(1, None)
        if self.state == State.DRAG_STARTED:
            if self.line_elem.segment.line.dt2 == 0:
                self._go_idle()
                return

            self.workspace.doc.elem_add(self.line_elem)
            self.line_elem = None
            self.state     = State.IDLE

    def handle_mouse_moved(self, p):
        if self.state == State.IDLE:
            self.coordinates_inspector.set_coord(0, p)
        elif self.state == State.DRAG_STARTED:
            self.coordinates_inspector.set_coord(1, p)
            self.line_elem.move_line(self.line_elem.segment.line.p0, p)

    def handle_elem_handles_changed(self, _elem, _handles):
        pass
