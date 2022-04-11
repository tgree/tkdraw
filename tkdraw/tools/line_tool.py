from enum import Enum

from .tool import Tool


class State(Enum):
    IDLE         = 0
    DRAG_STARTED = 1


class LineTool(Tool):
    def __init__(self, workspace, x, y, w, h, *args, **kwargs):
        super().__init__(workspace, x, y, w, h, *args, **kwargs)
        self.state      = State.IDLE
        self.drag_start = None
        self.drag_end   = None
        self.drag_line  = None
        self.icon_line  = workspace.tool_canvas.add_line(x + 10, y + 10,
                                                         w - 20, h - 20)

    def _go_idle(self):
        if self.state == State.DRAG_STARTED:
            self.workspace.delete_line(self.drag_line)
            self.drag_start = None
            self.drag_end   = None
            self.drag_line  = None
            self.state      = State.IDLE

    def handle_app_activated(self):
        assert self.state == State.IDLE

    def handle_app_deactivated(self):
        self._go_idle()

    def handle_tool_selected(self):
        assert self.state == State.IDLE

    def handle_tool_deselected(self):
        self._go_idle()

    def handle_canvas_entered(self):
        self.workspace._root.configure(cursor='tcross')

    def handle_canvas_exited(self):
        self.workspace._root.configure(cursor='arrow')

    def handle_key_pressed(self, e):
        if self.state == State.DRAG_STARTED:
            if e.keysym == 'Escape':
                self._go_idle()

    def handle_mouse_down(self, x, y):
        assert self.state == State.IDLE
        self.drag_start = (x, y)
        self.drag_end   = (x, y)
        self.drag_line  = self.workspace.add_line(x, y, 0, 0)
        self.state      = State.DRAG_STARTED

    def handle_mouse_up(self, x, y):
        if self.state == State.DRAG_STARTED:
            self.drag_start = None
            self.drag_end   = None
            self.drag_line  = None
            self.state      = State.IDLE

    def handle_mouse_moved(self, x, y):
        if self.state == State.DRAG_STARTED:
            self.drag_end = (x, y)
            self.workspace.move_line(self.drag_line,
                                     self.drag_start[0],
                                     self.drag_start[1],
                                     x - self.drag_start[0],
                                     y - self.drag_start[1])
