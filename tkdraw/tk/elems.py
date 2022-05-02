import tkinter
import ctypes


class Elem:
    def __init__(self, elem_id):
        self._elem_id = elem_id


class CanvasElem(Elem):
    def __init__(self, canvas, elem_id, x, y, width=None, height=None):
        super().__init__(elem_id)
        self._canvas = canvas
        self.x       = x
        self.y       = y
        if width is not None:
            self.width = width
            self.lx    = x
            self.rx    = x + width
        if height is not None:
            self.height = height
            self.ty     = y
            self.by     = y + height

    def configure(self, **kwargs):
        return self._canvas._canvas.itemconfig(self._elem_id, **kwargs)

    def cget(self, config):
        return self._canvas._canvas.itemcget(self._elem_id, config)

    def bbox(self):
        return self._canvas._bbox(self)

    def tag_lower(self, bottom_elem):
        self._canvas._tag_lower(self, bottom_elem)

    def set_fill(self, fill):
        self._canvas._set_fill(self, fill)

    def hide(self):
        self._canvas._hide(self)

    def show(self):
        self._canvas._show(self)

    def contains(self, x, y):
        w = getattr(self, 'width', 0)
        h = getattr(self, 'height', 0)
        return self.x <= x <= self.x + w and self.y <= y <= self.y + h

    def distance_squared(self, x, y):
        cx = self.x + getattr(self, 'width', 0) / 2
        cy = self.y + getattr(self, 'height', 0) / 2
        dx = (x - cx)
        dy = (y - cy)
        return dx*dx + dy*dy

    def move_to(self, x, y):
        self.x = x
        self.y = y
        if hasattr(self, 'height'):
            self.coords(x, y, x + self.width, y + self.height)
        else:
            self.coords(x, y)

    def resize(self, R):
        assert hasattr(self, 'width')
        assert hasattr(self, 'height')
        self.x      = R.p0.x
        self.y      = R.p0.y
        self.width  = R.width
        self.height = R.height
        self.coords(R.p0.x, R.p0.y, R.p1.x, R.p1.y)

    def coords(self, *args):
        self._canvas._coords(self, *args)


class TextElem(CanvasElem):
    def set_text(self, text):
        self._canvas._set_text(self, text)


class LineElem(CanvasElem):
    def move_line(self, x, y, dx, dy):
        self.coords(x, y, x + dx, y + dy)


class Widget:
    def __init__(self, widget):
        self._widget = widget


class Entry(Widget):
    def focus_set(self):
        self._widget.focus_set()


class Canvas:
    def __init__(self, workspace, canvas, w, h):
        self._workspace = workspace
        self._canvas    = canvas
        self.width      = w
        self.height     = h

    def _bbox(self, elem):
        return self._canvas.bbox(elem._elem_id)

    def _tag_lower(self, bottom_elem, top_elem):
        self._canvas.tag_lower(bottom_elem._elem_id, top_elem._elem_id)

    def _hide(self, elem):
        self._canvas.itemconfig(elem._elem_id, state='hidden')

    def _show(self, elem):
        self._canvas.itemconfig(elem._elem_id, state='normal')

    def _set_fill(self, elem, fill):
        self._canvas.itemconfig(elem._elem_id, fill=fill)

    def _coords(self, elem, *args):
        self._canvas.coords(elem._elem_id, *args)

    def _set_text(self, elem, text):
        self._canvas.itemconfig(elem._elem_id, text=text)

    @staticmethod
    def _vertices_to_args(vertices):
        min_x = min(v[0] for v in vertices)
        max_x = max(v[0] for v in vertices)
        min_y = min(v[1] for v in vertices)
        max_y = max(v[1] for v in vertices)
        w     = max_x - min_x
        h     = max_y - min_y
        args  = []
        for v in vertices:
            args.append(v[0])
            args.append(v[1])
        return args, min_x, min_y, w, h

    def add_lines(self, vertices, **kwargs):
        args, min_x, min_y, w, h = self._vertices_to_args(vertices)
        elem_id = self._canvas.create_line(*args, **kwargs)
        return LineElem(self, elem_id, min_x, min_y, w, h)

    def add_line(self, p0, p1, **kwargs):
        return self.add_lines([(p0.x, p0.y), (p1.x, p1.y)], **kwargs)

    def add_rectangle(self, R, **kwargs):
        elem_id = self._canvas.create_rectangle(
                (R.p0.x, R.p0.y, R.p1.x, R.p1.y), **kwargs)
        return CanvasElem(self, elem_id, R.p0.x, R.p0.y, width=R.width,
                          height=R.height)

    def add_poly(self, vertices, **kwargs):
        args, min_x, min_y, w, h = self._vertices_to_args(vertices)
        elem_id = self._canvas.create_polygon(*args, **kwargs)
        return CanvasElem(self, elem_id, min_x, min_y, w, h)

    def add_oval(self, x, y, width, height, **kwargs):
        elem_id = self._canvas.create_oval(
                (x, y, x + width, y + height), **kwargs)
        return CanvasElem(self, elem_id, x, y, width=width, height=height)

    def add_text(self, x, y, **kwargs):
        elem_id = self._canvas.create_text((x, y), **kwargs)
        return TextElem(self, elem_id, x, y)

    def add_window(self, x, y, widget, **kwargs):
        self._canvas.create_window(x, y, window=widget._widget, **kwargs)

    def delete(self, tag_or_id):
        self._canvas.delete(tag_or_id)

    def delete_elem(self, elem):
        self.delete(elem._elem_id)

    def add_entry(self, **kwargs):
        return Entry(tkinter.Entry(self._canvas, **kwargs))

    def register_handler(self, event_type, handler):
        self._canvas.bind(event_type, handler)


class TKBase:
    def __init__(self):
        # Windows hack #1.
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except AttributeError:
            pass
        self._root = tkinter.Tk()

        # Windows hack #2.
        self._root.tk.call('tk', 'scaling', 1.0)

    def set_geometry(self, x, y, width, height):
        self._root.geometry('%ux%u+%u+%u' % (width, height, x, y))

    def get_geometry(self):
        g = self._root.geometry()
        w, g    = g.split('x')
        h, x, y = g.split('+')
        return int(x), int(y), int(w), int(h)

    def mainloop(self):
        self._root.mainloop()

    def add_canvas(self, width, height, column=0, row=0, sticky=None,
                   _cls=Canvas):
        c = tkinter.Canvas(self._root, bd=0, highlightthickness=0, width=width,
                           height=height)
        c.grid(column=column, row=row, sticky=sticky)
        return _cls(self, c, width, height)

    def register_handler(self, event_type, handler):
        self._root.bind(event_type, handler)

    def register_mouse_handler(self, event_type, handler):
        self.register_handler(event_type, lambda e: handler(self, e, e.x, e.y))

    def register_mouse_moved(self, handler):
        self.register_mouse_handler('<Motion>', handler)

    def register_mouse_down(self, handler):
        self.register_mouse_handler('<Button-1>', handler)

    def register_mouse_up(self, handler):
        self.register_mouse_handler('<ButtonRelease-1>', handler)
