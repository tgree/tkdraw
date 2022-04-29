from enum import Enum

from .tool import Tool
from ..elems import LineElem


class State(Enum):
    IDLE         = 0
    DRAG_STARTED = 1


class LineTool(Tool):
    def __init__(self, workspace, x, y, w, h, *args, **kwargs):
        super().__init__(workspace, x, y, w, h, *args, **kwargs)
        self.state     = State.IDLE
        self.line_elem = None
        self.icon_line = workspace.tool_canvas.add_line(x + 10, y + 10,
                                                        w - 20, h - 20)

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
        tk_elem        = self.workspace.add_line(p.x, p.y, 0, 0)
        self.line_elem = LineElem(tk_elem, p, p)
        self.state     = State.DRAG_STARTED

    def handle_mouse_up(self, p):
        if self.state == State.DRAG_STARTED:
            if self.line_elem.segment.line.dt2 == 0:
                self._go_idle()
                return

            self.workspace.doc.add_elem(self.line_elem)
            self.line_elem = None
            self.state     = State.IDLE

    def handle_mouse_moved(self, p):
        if self.state == State.DRAG_STARTED:
            self.line_elem.move_line(self.line_elem.segment.line.p0, p)
