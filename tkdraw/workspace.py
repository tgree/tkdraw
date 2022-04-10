from .tk_elems import TKBase, Canvas
from . import tools


WINDOW_X      = 50
WINDOW_Y      = 50
WINDOW_WIDTH  = 800
WINDOW_HEIGHT = 500

TOOLS_WIDTH  = 100
TOOLS_HEIGHT = 400

DRAW_WIDTH   = WINDOW_WIDTH - TOOLS_WIDTH
DRAW_HEIGHT  = WINDOW_HEIGHT
GRID_SPACING = 10


def clamp(l, v, r):
    return l if v < l else r if v > r else v


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
        self.border_rect   = self.add_rectangle(0, 0, 0, 0, outline='',
                                                fill='black')
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
        point.  This is O(M + N) and performance is snappy, at least on my
        M1 MacBook Pro.
        '''
        self.border_rect.resize(GRID_SPACING, GRID_SPACING, e.width - 1,
                                e.height - 1)
        self.width_points  = e.width // GRID_SPACING
        self.height_points = e.height // GRID_SPACING

        for y, r in enumerate(self.h_rects):
            r.resize(0, y * GRID_SPACING + 1, e.width, GRID_SPACING - 1)
        for y in range(len(self.h_rects), e.height // GRID_SPACING + 1):
            r = self.add_rectangle(0, y * GRID_SPACING + 1, e.width,
                                   GRID_SPACING - 1, fill='white', outline='')
            self.h_rects.append(r)

        for x, r in enumerate(self.v_rects):
            r.resize(x * GRID_SPACING + 1, 0, GRID_SPACING - 1, e.height)
        for x in range(len(self.v_rects), e.width // GRID_SPACING + 1):
            r = self.add_rectangle(x * GRID_SPACING + 1, 0, GRID_SPACING - 1,
                                   e.height, fill='white', outline='')
            self.v_rects.append(r)


class Workspace(TKBase):
    def __init__(self):
        super().__init__()

        self.set_geometry(WINDOW_X, WINDOW_Y, 800, 500)
        self.tool_canvas = self.add_canvas(TOOLS_WIDTH, TOOLS_HEIGHT, 0, 0,
                                           sticky='nws', _cls=ToolCanvas)

        self.canvas = self.add_canvas(DRAW_WIDTH, DRAW_HEIGHT, 1, 0,
                                      sticky='nsew', _cls=DrawCanvas)
        self._root.columnconfigure(1, weight=1)
        self._root.rowconfigure(0, weight=1)
        self._root.minsize(300, TOOLS_HEIGHT)

        self.register_mouse_down(self.handle_mouse_down)
        self.register_mouse_up(self.handle_mouse_up)
        self.register_mouse_moved(self.handle_mouse_moved)
        self.canvas.register_handler('<Enter>', self.handle_canvas_entered)
        self.canvas.register_handler('<Leave>', self.handle_canvas_exited)

        self.tools = [tools.LineTool(self)]
        self.selected_tool = self.tools[0]
        self.selected_tool.handle_tool_selected()

    def _handle_mouse_event(self, e, x, y, handler):
        if e.widget != self.canvas._canvas:
            return

        x = clamp(0, round(x / GRID_SPACING), self.canvas.width_points)
        y = clamp(0, round(y / GRID_SPACING), self.canvas.height_points)
        handler(x, y)

    def handle_mouse_down(self, _, e, x, y):
        self._handle_mouse_event(e, x, y, self.selected_tool.handle_mouse_down)

    def handle_mouse_up(self, _, e, x, y):
        self._handle_mouse_event(e, x, y, self.selected_tool.handle_mouse_up)

    def handle_mouse_moved(self, _, e, x, y):
        self._handle_mouse_event(e, x, y, self.selected_tool.handle_mouse_moved)

    def handle_canvas_entered(self, e):
        self.selected_tool.handle_canvas_entered()

    def handle_canvas_exited(self, e):
        self.selected_tool.handle_canvas_exited()

    def add_line(self, x, y, dx, dy):
        return self.canvas.add_line(x * GRID_SPACING, y * GRID_SPACING,
                                    dx * GRID_SPACING, dy * GRID_SPACING)

    def delete_line(self, l):
        self.canvas.delete_elem(l)

    def move_line(self, l, x, y, dx, dy):
        l.move_line(x * GRID_SPACING, y * GRID_SPACING,
                    dx * GRID_SPACING, dy * GRID_SPACING)
