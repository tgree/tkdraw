from .tool import Tool


class NearestTool(Tool):
    def __init__(self, workspace, x, y, w, h, *args, **kwargs):
        super().__init__(workspace, x, y, w, h, *args, **kwargs)
        self.icon_rect = workspace.tool_canvas.add_rectangle(
                x + 20, y + 20, 10, 10, fill='black')
        self.point = None

    def _go_idle(self):
        if self.point:
            self.workspace.delete_canvas_elem(self.point)
            self.point = None

    def handle_app_activated(self):
        pass

    def handle_app_deactivated(self):
        pass

    def handle_tool_selected(self):
        self.icon_border.configure(outline='black')

    def handle_tool_deselected(self):
        self._go_idle()
        self.icon_border.configure(outline='#CCCCCC')

    def handle_canvas_entered(self, p):
        self.point = self.workspace.canvas.add_rectangle(
                0, 0, 4, 4, fill='black')
        self.handle_mouse_moved(p)

    def handle_canvas_exited(self):
        self._go_idle()

    def handle_key_pressed(self, e):
        pass

    def handle_mouse_down(self, p):
        pass

    def handle_mouse_up(self, p):
        pass

    def handle_mouse_moved(self, p):
        if self.workspace.elems:
            px, py = self.workspace.elems[0].nearest_point(p.ex, p.ey)
            self.workspace.move_to(self.point, px, py, -2, -2)
