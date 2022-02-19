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
        self.border_line = self.add_line(TOOLS_WIDTH - 1, 0,
                                         0, TOOLS_HEIGHT - 1)
        self.register_handler('<Configure>', self.handle_config_change)

    def handle_config_change(self, e):
        self.border_line.move_line(TOOLS_WIDTH - 1, 0, 0, e.height - 1)


class DrawCanvas(Canvas):
    def __init__(self, workspace, canvas, width, height):
        super().__init__(workspace, canvas, width, height)
        self.grid_points = {}
        self.border_rect = self.add_rectangle(0, 0, DRAW_WIDTH - 1, 
                                              DRAW_HEIGHT - 1, outline='',
                                              fill='white')
        self.register_handler('<Configure>', self.handle_config_change)

    def handle_config_change(self, e):
        self.border_rect.resize(0, 0, e.width - 1, e.height - 1)

        for x in range(1, e.width // GRID_SPACING + 1):
            for y in range(1, e.height // GRID_SPACING + 1):
                p = (x, y)
                if p not in self.grid_points:
                    l = self.add_line(x * GRID_SPACING, y * GRID_SPACING, 1, 0)
                    self.grid_points[p] = l


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
