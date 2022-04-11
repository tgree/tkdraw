from .tk_elems import TKBase, Canvas
from . import tools


WINDOW_X      = 10
WINDOW_Y      = 50
TITLE_HEIGHT  = 28

TOOLS_WIDTH  = 100
TOOLS_HEIGHT = 400

GRID_SPACING = 10
GRID_PAD     = (GRID_SPACING // 2)


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
        self.content_rect  = self.add_rectangle(0, 0, 0, 0, outline='',
                                                fill='black')
        self.h_pad         = self.add_rectangle(0, 0, 0, 0, fill='white',
                                                outline='')
        self.v_pad         = self.add_rectangle(0, 0, 0, 0, fill='white',
                                                outline='')
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
        self.content_rect.resize(GRID_PAD - 1, GRID_PAD - 1, e.width - 1,
                                 e.height - 1)
        self.width_points  = (e.width - GRID_PAD - 1) // GRID_SPACING
        self.height_points = (e.height - GRID_PAD - 1) // GRID_SPACING

        self.h_pad.resize(0, 0, e.width, GRID_PAD)
        for y, r in enumerate(self.h_rects):
            r.resize(0, y * GRID_SPACING + GRID_PAD + 1, e.width,
                     GRID_SPACING - 1)
        for y in range(len(self.h_rects), e.height // GRID_SPACING + 1):
            r = self.add_rectangle(0, y * GRID_SPACING + GRID_PAD + 1, e.width,
                                   GRID_SPACING - 1, fill='white', outline='')
            self.h_rects.append(r)

        self.v_pad.resize(0, 0, GRID_PAD, e.height)
        for x, r in enumerate(self.v_rects):
            r.resize(x * GRID_SPACING + GRID_PAD + 1, 0, GRID_SPACING - 1,
                     e.height)
        for x in range(len(self.v_rects), e.width // GRID_SPACING + 1):
            r = self.add_rectangle(x * GRID_SPACING + GRID_PAD + 1, 0,
                                   GRID_SPACING - 1, e.height, fill='white',
                                   outline='')
            self.v_rects.append(r)


class Workspace(TKBase):
    def __init__(self):
        super().__init__()

        w  = (self._root.winfo_screenwidth() - 2*WINDOW_X)
        w -= (w % GRID_SPACING)
        h  = (self._root.winfo_screenheight() - TITLE_HEIGHT - WINDOW_Y -
              WINDOW_X)
        h -= (h % GRID_SPACING)

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

        self.tools = [tools.LineTool(self)]
        self.selected_tool = self.tools[0]
        self.selected_tool.handle_tool_selected()

    def _handle_mouse_event(self, e, x, y, handler):
        if e.widget != self.canvas._canvas:
            return

        x = clamp(0, round((x - GRID_PAD) / GRID_SPACING),
                  self.canvas.width_points)
        y = clamp(0, round((y - GRID_PAD) / GRID_SPACING),
                  self.canvas.height_points)
        handler(x, y)

    def handle_mouse_down(self, _, e, x, y):
        self._handle_mouse_event(e, x, y, self.selected_tool.handle_mouse_down)

    def handle_mouse_up(self, _, e, x, y):
        self._handle_mouse_event(e, x, y, self.selected_tool.handle_mouse_up)

    def handle_mouse_moved(self, _, e, x, y):
        self._handle_mouse_event(e, x, y, self.selected_tool.handle_mouse_moved)

    def handle_key_pressed(self, e):
        self.selected_tool.handle_key_pressed(e)

    def handle_canvas_entered(self, _e):
        self.selected_tool.handle_canvas_entered()

    def handle_canvas_exited(self, _e):
        self.selected_tool.handle_canvas_exited()

    def handle_config_change(self, e):
        if e.widget != self._root:
            return
        if e.height == 1:
            return

        h = (e.height - (e.height % GRID_SPACING))
        w = (e.width - (e.width % GRID_SPACING))
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

    def add_line(self, x, y, dx, dy):
        return self.canvas.add_line(x * GRID_SPACING + GRID_PAD,
                                    y * GRID_SPACING + GRID_PAD,
                                    dx * GRID_SPACING, dy * GRID_SPACING)

    def delete_line(self, l):
        self.canvas.delete_elem(l)

    @staticmethod
    def move_line(l, x, y, dx, dy):
        l.move_line(x * GRID_SPACING + GRID_PAD, y * GRID_SPACING + GRID_PAD,
                    dx * GRID_SPACING, dy * GRID_SPACING)
