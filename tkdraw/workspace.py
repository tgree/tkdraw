from .tk_elems import TKBase, Canvas


WINDOW_X      = 50
WINDOW_Y      = 50
WINDOW_WIDTH  = 800
WINDOW_HEIGHT = 500

TOOLS_WIDTH  = 100
TOOLS_HEIGHT = 400

DRAW_WIDTH   = WINDOW_WIDTH - TOOLS_WIDTH
DRAW_HEIGHT  = WINDOW_HEIGHT
GRID_SPACING = 10


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
        self.h_rects     = []
        self.v_rects     = []
        self.border_rect = self.add_rectangle(0, 0, 0, 0, outline='',
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

        self.drag_start = None
        self.drag_end   = None
        self.drag_line  = None

        self.register_mouse_down(self.handle_mouse_down)
        self.register_mouse_up(self.handle_mouse_up)
        self.register_mouse_moved(self.handle_mouse_moved)

    def handle_mouse_down(self, _, e, x, y):
        if e.widget != self.canvas._canvas:
            return

        assert self.drag_line is None
        x               = x // GRID_SPACING
        y               = y // GRID_SPACING
        self.drag_start = (x, y)
        self.drag_end   = (x, y)
        self.drag_line  = self.canvas.add_line(x * GRID_SPACING,
                                               y * GRID_SPACING,
                                               0, 0)

    def handle_mouse_up(self, _, e, x, y):
        self.drag_start = None
        self.drag_end   = None
        self.drag_line  = None

    def handle_mouse_moved(self, _, e, x, y):
        if self.drag_line is None:
            return
        if e.widget != self.canvas._canvas:
            return

        x              = x // GRID_SPACING
        y              = y // GRID_SPACING
        self.drag_end  = (x, y)
        self.drag_line.move_line(self.drag_start[0] * GRID_SPACING,
                                 self.drag_start[1] * GRID_SPACING,
                                 (x - self.drag_start[0]) * GRID_SPACING,
                                 (y - self.drag_start[1]) * GRID_SPACING)
