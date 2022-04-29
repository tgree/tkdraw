from .tk.elems import TKBase, Canvas
from . import tools
from . import coords


WINDOW_X      = 10
WINDOW_Y      = 50
TITLE_HEIGHT  = 28

TOOL_DIM     = 50
TOOLS_WIDTH  = 2 * TOOL_DIM
TOOLS_HEIGHT = 400


def clamp(l, v, r):
    return l if v < l else r if v > r else v


class MousePoint:
    def __init__(self, x, y, ex, ey):
        self.x  = x
        self.y  = y
        self.ex = ex
        self.ey = ey


class ToolCanvas(Canvas):
    def __init__(self, workspace, canvas, width, height):
        super().__init__(workspace, canvas, width, height)
        self.border_line = self.add_line(TOOLS_WIDTH - 1, 1,
                                         0, TOOLS_HEIGHT - 2)
        self.register_handler('<Configure>', self.handle_config_change)

    def handle_config_change(self, e):
        self.border_line.move_line(TOOLS_WIDTH - 1, 1, 0, e.height - 2)


class DrawCanvas(Canvas):
    def __init__(self, workspace, canvas, width, height):
        super().__init__(workspace, canvas, width, height)
        self.h_rects       = []
        self.v_rects       = []
        self.width_points  = None
        self.height_points = None
        self.content_rect  = self.add_rectangle(0, 0, 0, 0, outline='',
                                                fill='black')
        self.h_pad         = self.add_rectangle(0, 0, 0, 0, fill='white',
                                                outline='')
        self.v_pad         = self.add_rectangle(0, 0, 0, 0, fill='white',
                                                outline='')
        self.grid_shown    = True
        self.register_handler('<Configure>', self._handle_config_change)

    def _handle_config_change(self, e):
        '''
        Called when the canvas size changes.  Mainly this deals with drawing
        the grid on the canvas.  The naive algorithm is O(MN) and draws a
        single pixel at each grid point.  As the window gets large, the
        performance tanks incredibly badly with that algorithm.

        Instead, we start with a black rectangle covering the entire canvas
        and then draw white horizontal bands spaced to carve out horizontal
        lines from the black rectangle and then we draw white vertical bands
        spaced to cut the black lines up into individual pixels at each grid
        point.  This is O(M + N) and performance is snappy, even on my old 2012
        Macbook Air.
        '''
        self.content_rect.resize(0, 0, e.width - 1, e.height - 1)
        self.width_points, self.height_points = coords.canvas_to_grid_floor(
            e.width - 1, e.height - 1)

        h_bands = coords.get_canvas_h_bands(e.width, e.height)
        for i, (x, y, w, h) in enumerate(h_bands):
            if i < len(self.h_rects):
                self.h_rects[i].resize(x, y, w, h)
            else:
                r = self.add_rectangle(x, y, w, h, fill='white', outline='')
                self.h_rects.append(r)

        v_bands = coords.get_canvas_v_bands(e.width, e.height)
        for i, (x, y, w, h) in enumerate(v_bands):
            if i < len(self.v_rects):
                self.v_rects[i].resize(x, y, w, h)
            else:
                r = self.add_rectangle(x, y, w, h, fill='white', outline='')
                self.v_rects.append(r)

    def hide_grid(self):
        self.content_rect.set_fill('white')
        for r in self.h_rects:
            r.hide()
        for r in self.v_rects:
            r.hide()
        self.grid_shown = False

    def show_grid(self):
        self.content_rect.set_fill('black')
        for r in self.h_rects:
            r.show()
        for r in self.v_rects:
            r.show()
        self.grid_shown = True

    def toggle_grid(self):
        if self.grid_shown:
            self.hide_grid()
        else:
            self.show_grid()


class Workspace(TKBase):
    def __init__(self):
        super().__init__()

        w = coords.canvasx_floor(self._root.winfo_screenwidth() - 2*WINDOW_X)
        h = coords.canvasy_floor(self._root.winfo_screenheight() -
                                 TITLE_HEIGHT - WINDOW_Y - WINDOW_X)

        self.set_geometry(WINDOW_X, WINDOW_Y, w, h)
        self.tool_canvas = self.add_canvas(TOOLS_WIDTH, TOOLS_HEIGHT, 0, 0,
                                           sticky='nws', _cls=ToolCanvas)

        self.canvas = self.add_canvas(1, 1, 1, 0, sticky='nsew',
                                      _cls=DrawCanvas)
        self._root.columnconfigure(1, weight=1)
        self._root.rowconfigure(0, weight=1)
        self._root.minsize(300, TOOLS_HEIGHT)

        self.register_mouse_down(self.handle_mouse_down)
        self.register_mouse_up(self.handle_mouse_up)
        self.register_mouse_moved(self.handle_mouse_moved)
        self.register_handler('<KeyPress>', self.handle_key_pressed)
        self.register_handler('<Configure>', self.handle_config_change)
        self.register_handler('<Activate>', self.handle_activate)
        self.register_handler('<Deactivate>', self.handle_deactivate)
        self.canvas.register_handler('<Enter>', self.handle_canvas_entered)
        self.canvas.register_handler('<Leave>', self.handle_canvas_exited)

        self.elems = []

        self.tools = []
        self.selected_tool = None

        tool_classes = [tools.NullTool,
                        tools.LineTool,
                        tools.NearestTool,
                        ]
        for i, tcls in enumerate(tool_classes):
            x = (i % 2) * TOOL_DIM
            y = (i // 2) * TOOL_DIM
            t = tcls(self, x, y, TOOL_DIM - 2, TOOL_DIM - 2)
            self.tools.append(t)

        self.select_tool(self.tools[0])

    def select_tool(self, t):
        if self.selected_tool:
            self.selected_tool.handle_tool_deselected()
        self.selected_tool = t
        if self.selected_tool:
            self.selected_tool.handle_tool_selected()

    def _handle_mouse_event(self, e, x, y, handler):
        if e.widget != self.canvas._canvas:
            return

        ex = clamp(0, coords.canvasx_to_gridx_float(x),
                   self.canvas.width_points)
        ey = clamp(0, coords.canvasy_to_gridy_float(y),
                   self.canvas.height_points)
        x  = clamp(0, coords.canvasx_to_gridx_round(x),
                   self.canvas.width_points)
        y  = clamp(0, coords.canvasy_to_gridy_round(y),
                   self.canvas.height_points)
        handler(MousePoint(x, y, ex, ey))

    def _handle_tool_mouse_down(self, _e, x, y):
        i = (y // TOOL_DIM) * 2 + (x // TOOL_DIM)
        if i < len(self.tools):
            self.select_tool(self.tools[i])

    def handle_mouse_down(self, _, e, x, y):
        if e.widget == self.tool_canvas._canvas:
            self._handle_tool_mouse_down(e, x, y)
        else:
            self._handle_mouse_event(e, x, y,
                                     self.selected_tool.handle_mouse_down)

    def handle_mouse_up(self, _, e, x, y):
        self._handle_mouse_event(e, x, y, self.selected_tool.handle_mouse_up)

    def handle_mouse_moved(self, _, e, x, y):
        self._handle_mouse_event(e, x, y, self.selected_tool.handle_mouse_moved)

    def handle_key_pressed(self, e):
        if e.char in ('g', 'G'):
            self.canvas.toggle_grid()
        else:
            self.selected_tool.handle_key_pressed(e)

    def handle_canvas_entered(self, e):
        self._handle_mouse_event(e, e.x, e.y,
                                 self.selected_tool.handle_canvas_entered)

    def handle_canvas_exited(self, _e):
        self.selected_tool.handle_canvas_exited()

    def handle_config_change(self, e):
        if e.widget != self._root:
            return
        if e.height == 1:
            return

        h = coords.canvasy_floor(e.height)
        w = coords.canvasx_floor(e.width)
        if e.height != h or e.width != w:
            x, y, _, _ = self.get_geometry()
            self.set_geometry(x, y, w, h)

    def handle_activate(self, e):
        if e.widget != self._root:
            return
        self.selected_tool.handle_app_activated()

    def handle_deactivate(self, e):
        if e.widget != self._root:
            return
        self.selected_tool.handle_app_deactivated()

    def add_elem(self, elem):
        self.elems.append(elem)

    def add_line(self, x, y, dx, dy):
        return self.canvas.add_line(coords.gridx_to_canvasx(x),
                                    coords.gridy_to_canvasy(y),
                                    coords.grid_to_canvas_delta(dx),
                                    coords.grid_to_canvas_delta(dy))

    def add_rectangle(self, x, y, fine_dx, fine_dy, w, h, **kwargs):
        return self.canvas.add_rectangle(
                coords.gridx_to_canvasx(x) + fine_dx,
                coords.gridy_to_canvasy(y) + fine_dy,
                w, h, **kwargs)

    def delete_canvas_elem(self, l):
        self.canvas.delete_elem(l)
