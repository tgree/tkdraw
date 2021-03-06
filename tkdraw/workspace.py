import tkinter.font

from .tk.elems import TKBase, Canvas
from . import tools
from . import coords
from . import geom
from . import document


WINDOW_X      = 10
WINDOW_Y      = 50
TITLE_HEIGHT  = 28
BOTTOM_SPACE  = 200

TOOL_DIM     = 50
TOOLS_WIDTH  = 2 * TOOL_DIM
TOOLS_HEIGHT = 400

INSPECT_WIDTH  = 200
INSPECT_HEIGHT = 400


def clamp(l, v, r):
    return l if v < l else r if v > r else v


class MousePoint(geom.Vec):
    def __init__(self, x, y, ex, ey, modifiers):
        super().__init__(x, y)
        self.ex        = ex
        self.ey        = ey
        self.modifiers = modifiers


class ToolCanvas(Canvas):
    def __init__(self, workspace, canvas, width, height):
        super().__init__(workspace, canvas, width, height)
        self.border_line = self.add_line(
                geom.Vec(TOOLS_WIDTH - 1, 1),
                geom.Vec(TOOLS_WIDTH - 1, TOOLS_HEIGHT - 1))
        self.register_handler('<Configure>', self.handle_config_change)

    def handle_config_change(self, e):
        self.border_line.move_line(TOOLS_WIDTH - 1, 1, 0, e.height - 2)


class InspectCanvas(Canvas):
    def __init__(self, workspace, canvas, width, height):
        super().__init__(workspace, canvas, width, height)
        self.workspace = workspace
        self.border_line = self.add_line(
                geom.Vec(0, 1), geom.Vec(0, INSPECT_HEIGHT - 2))
        self.text_y      = None
        self._entries    = []
        self.label_font  = tkinter.font.Font(family='Arial', size=12,
                                             weight='bold')
        self.header_font = tkinter.font.Font(family='Arial', size=10,
                                             weight='bold')
        self.field_font  = tkinter.font.Font(family='Arial', size=10)

        self.register_handler('<Configure>', self.handle_config_change)

    def handle_config_change(self, e):
        self.border_line.move_line(0, 1, 0, e.height - 2)

    def clear(self):
        self.text_y = 3
        self.workspace.canvas.focus_set()
        for e in self._entries:
            e.destroy()
        for e in self._canvas.find_all():
            if e != self.border_line._elem_id:
                self.delete(e)
        self._entries = []

    def iadd_title(self, text):
        elem = self.add_text(geom.Vec(3, self.text_y), text=text, anchor='nw',
                             font=self.label_font)
        self.text_y += 14
        return elem

    def iadd_header(self, text):
        elem = self.add_text(geom.Vec(3, self.text_y + 2), text=text,
                             anchor='nw', font=self.header_font)
        self.text_y += 14
        return elem

    def iadd_field(self, text):
        elem = self.add_text(geom.Vec(10, self.text_y), text=text, anchor='nw',
                             font=self.field_font)
        self.text_y += 12
        return elem

    def iadd_entry(self, **kwargs):
        elem = self.add_entry(font=self.field_font, **kwargs)
        elem.configure(highlightthickness=3)
        self.add_window(10, self.text_y, elem, anchor='nw',
                        width=INSPECT_WIDTH-10-4)
        self.text_y += 18
        self._entries.append(elem)
        return elem

    def iadd_multiline_entry(self, nlines=1, **kwargs):
        elem = self.add_multiline_entry(font=self.field_font, **kwargs)
        elem.configure(highlightthickness=1)
        h = self.field_font.metrics('linespace') * nlines
        self.add_window(10, self.text_y, elem, anchor='nw',
                        width=INSPECT_WIDTH-10-4, height=h+4)
        self.text_y += 24
        self._entries.append(elem)
        return elem


class DrawCanvas(Canvas):
    def __init__(self, workspace, canvas, width, height):
        super().__init__(workspace, canvas, width, height)
        self.h_rects       = []
        self.v_rects       = []
        self.width_points  = None
        self.height_points = None
        self.grid_shown    = True

        z_rect            = geom.Rect.zero()
        self.content_rect = self.add_rectangle(z_rect, outline='', fill='black')
        self.h_pad        = self.add_rectangle(z_rect, fill='white', outline='')
        self.v_pad        = self.add_rectangle(z_rect, fill='white', outline='')

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
        self.content_rect.resize(geom.Rect.from_vec(
            geom.Vec(e.width - 1, e.height - 1)))
        self.width_points, self.height_points = coords.canvas_to_grid_floor(
            e.width - 1, e.height - 1)

        h_bands = coords.get_canvas_h_bands(e.width, e.height)
        for i, R in enumerate(h_bands):
            if i < len(self.h_rects):
                self.h_rects[i].resize(R)
            else:
                r = self.add_rectangle(R, fill='white', outline='')
                self.h_rects.append(r)

        v_bands = coords.get_canvas_v_bands(e.width, e.height)
        for i, R in enumerate(v_bands):
            if i < len(self.v_rects):
                self.v_rects[i].resize(R)
            else:
                r = self.add_rectangle(R, fill='white', outline='')
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
                                 TITLE_HEIGHT - WINDOW_Y - WINDOW_X -
                                 BOTTOM_SPACE)

        self.set_geometry(WINDOW_X, WINDOW_Y, w, h)
        self.tool_canvas = self.add_canvas(TOOLS_WIDTH, TOOLS_HEIGHT, 0, 0,
                                           sticky='nws', _cls=ToolCanvas)
        self.canvas = self.add_canvas(1, 1, 1, 0, sticky='nsew',
                                      _cls=DrawCanvas)
        self.inspect_canvas = self.add_canvas(INSPECT_WIDTH, INSPECT_HEIGHT,
                                              2, 0, sticky='nes',
                                              _cls=InspectCanvas)

        self._root.columnconfigure(1, weight=1)
        self._root.rowconfigure(0, weight=1)
        self._root.minsize(TOOLS_WIDTH + INSPECT_WIDTH + 200, TOOLS_HEIGHT)

        self.register_mouse_down(self.handle_mouse_down)
        self.register_mouse_up(self.handle_mouse_up)
        self.register_mouse_moved(self.handle_mouse_moved)
        self.register_handler('<Configure>', self.handle_config_change)
        self.register_handler('<Activate>', self.handle_activate)
        self.register_handler('<Deactivate>', self.handle_deactivate)
        self.canvas.register_handler('<KeyPress>', self.handle_key_pressed)
        self.canvas.register_handler('<Enter>', self.handle_canvas_entered)
        self.canvas.register_handler('<Leave>', self.handle_canvas_exited)
        self.canvas.focus_set()

        self.doc = document.Document()

        self.tools = []
        self.selected_tool = None

        tool_classes = [tools.SelectionTool,
                        tools.LineTool,
                        tools.TextTool,
                        tools.NullTool,
                        ]
        for i, tcls in enumerate(tool_classes):
            x = (i % 2) * TOOL_DIM
            y = (i // 2) * TOOL_DIM
            R = geom.Rect(geom.Vec(x, y),
                          geom.Vec(x + TOOL_DIM - 2, y + TOOL_DIM - 2))
            t = tcls(self, R)
            self.tools.append(t)

        self.select_tool(self.tools[0])

    def select_tool(self, t):
        if self.selected_tool:
            self.selected_tool.handle_tool_deselected()
        self.inspect_canvas.clear()
        self.selected_tool = t
        if self.selected_tool:
            self.inspect_canvas.iadd_title(t.INSPECT_TITLE)
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
        handler(MousePoint(x, y, ex, ey, e.state))

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

    def notify_handles_changed(self, elem, handles):
        self.selected_tool.handle_elem_handles_changed(elem, handles)

    def add_line(self, p0, p1):
        '''
        Add a line in grid coordinates to the workspace.
        '''
        return self.canvas.add_line(coords.gridp_to_canvasp(p0),
                                    coords.gridp_to_canvasp(p1))

    def add_text(self, p0, **kwargs):
        '''
        Add a text item in grid coordinates to the workspace.
        '''
        return self.canvas.add_text(coords.gridp_to_canvasp(p0), **kwargs)

    def add_rectangle(self, R, **kwargs):
        '''
        Add a rectangle in grid coordinates to the workspace.
        '''
        R = geom.Rect(coords.gridp_to_canvasp(R.p0),
                      coords.gridp_to_canvasp(R.p1))
        return self.canvas.add_rectangle(R, **kwargs)

    def add_fine_rectangle(self, P, R, **kwargs):
        '''
        Add a rectangle finely sized in canvas coordinates centered at the
        grid point P to the workspace.
        '''
        P = coords.gridp_to_canvasp(P)
        return self.canvas.add_rectangle(R + P, **kwargs)

    def delete_canvas_elem(self, l):
        self.canvas.delete_elem(l)
