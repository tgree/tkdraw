from .tool import Tool


class NearestTool(Tool):
    def __init__(self, workspace, x, y, w, h, *args, **kwargs):
        super().__init__(workspace, x, y, w, h, *args, **kwargs)
        self.nearest_elem     = None
        self.nearest_points   = []
        self.selected_elem    = None
        self.selected_points  = []
        self.last_mouse_point = None
        self.icon_rect = workspace.tool_canvas.add_rectangle(
                x + 20, y + 20, 10, 10, fill='black')

    def _add_selected_points(self):
        for h in self.selected_elem.handles:
            self.selected_points.append(self.workspace.add_rectangle(
                h[0], h[1], -2, -2, 4, 4, fill='black'))

    def _remove_selected_points(self):
        for p in self.selected_points:
            self.workspace.delete_canvas_elem(p)
        self.selected_points = []

    def _add_nearest_points(self, p):
        if not self.workspace.elems:
            return

        nearest = None
        for e in self.workspace.elems:
            px, py = e.nearest_point(p.ex, p.ey)
            d_2    = (p.ex - px)**2 + (p.ey - py)**2
            if not nearest or d_2 < nearest[0]:
                nearest = (d_2, px, py, e)

        if nearest[0] >= 4:
            self._remove_nearest_points()
            self.nearest_elem = None
            return

        if nearest[3] == self.nearest_elem:
            return
        
        self._remove_nearest_points()
        self.nearest_elem = nearest[3]
        for h in self.nearest_elem.handles:
            self.nearest_points.append(self.workspace.add_rectangle(
                h[0], h[1], -3, -3, 6, 6))

    def _remove_nearest_points(self):
        for p in self.nearest_points:
            self.workspace.delete_canvas_elem(p)
        self.nearest_points = []

    def _go_idle(self):
        self._remove_nearest_points()
        self.nearest_elem  = None

        self._remove_selected_points()
        self.selected_elem = None

        self.last_mouse_point = None

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
        self.handle_mouse_moved(p)

    def handle_canvas_exited(self):
        self._remove_nearest_points()
        self.nearest_elem     = None
        self.last_mouse_point = None

    def handle_key_pressed(self, e):
        if not self.selected_elem:
            return

        if e.keysym in ('Left', 'Right', 'Up', 'Down'):
            if e.keysym == 'Left':
                self.selected_elem.nudge(-1, 0)
            elif e.keysym == 'Right':
                self.selected_elem.nudge(1, 0)
            elif e.keysym == 'Up':
                self.selected_elem.nudge(0, -1)
            elif e.keysym == 'Down':
                self.selected_elem.nudge(0, 1)

            self._remove_selected_points()
            self._add_selected_points()
            if self.nearest_elem:
                self._remove_nearest_points()
                self.nearest_elem = None
            if self.last_mouse_point:
                self._add_nearest_points(self.last_mouse_point)

    def handle_mouse_down(self, p):
        for p in self.selected_points:
            self.workspace.delete_canvas_elem(p)
        self.selected_points = []

        self.selected_elem = self.nearest_elem
        if self.selected_elem:
            self._add_selected_points()

    def handle_mouse_up(self, p):
        pass

    def handle_mouse_moved(self, p):
        self.last_mouse_point = p
        self._add_nearest_points(p)
