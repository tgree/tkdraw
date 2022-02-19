import tkinter


def point_in_box(px, py, x0, y0, width, height):
    return (x0 <= px <= x0 + width and y0 <= py <= y0 + height)


class Elem:
    def __init__(self, canvas, elem_id, x, y, width=None, height=None):
        self.canvas  = canvas
        self.elem_id = elem_id
        self.x       = x
        self.y       = y
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height

    def bbox(self):
        return self.canvas.canvas.bbox(self.elem_id)

    def tag_lower(self, other_elem):
        self.canvas.canvas.tag_lower(self.elem_id, other_elem.elem_id)

    def set_fill(self, fill):
        self.canvas.canvas.itemconfig(self.elem_id, fill=fill)


class BoundedElem(Elem):
    def contains(self, x, y):
        return point_in_box(x, y, self.x, self.y, self.width, self.height)

    def distance_squared(self, x, y):
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        dx = (x - cx)
        dy = (y - cy)
        return dx*dx + dy*dy

    def move_to(self, x, y):
        self.x = x
        self.y = y
        self.canvas.canvas.coords(self.elem_id,
                                  x, y, x + self.width, y + self.height)

    def resize(self, x, y, width, height):
        self.x      = x
        self.y      = y
        self.width  = width
        self.height = height
        self.canvas.canvas.coords(self.elem_id, x, y, x + width, y + height)


class Rectangle(BoundedElem):
    def __init__(self, canvas, x, y, width, height, **kwargs):
        elem_id = canvas.canvas.create_rectangle(
                (x, y, x + width, y + height), **kwargs)
        super().__init__(canvas, elem_id, x, y, width=width, height=height)


class Oval(BoundedElem):
    def __init__(self, canvas, x, y, width, height, **kwargs):
        elem_id = canvas.canvas.create_oval(
                (x, y, x + width, y + height), **kwargs)
        super().__init__(canvas, elem_id, x, y, width=width, height=height)


class Text(Elem):
    def __init__(self, canvas, x, y, **kwargs):
        elem_id = canvas.canvas.create_text((x, y), **kwargs)
        super().__init__(canvas, elem_id, x, y)

    def set_text(self, text):
        self.canvas.canvas.itemconfig(self.elem_id, text=text)

    def set_fill(self, fill):
        self.canvas.canvas.itemconfig(self.elem_id, fill=fill)


class Canvas:
    def __init__(self, workspace, width, height, column, row, sticky):
        self.workspace = workspace
        self.canvas = tkinter.Canvas(workspace.root, bd=0,
                                     highlightthickness=0,
                                     width=width, height=height)
        #self.canvas.pack(fill='both', expand=True)
        self.canvas.grid(column=column, row=row, sticky=sticky)
        #self.canvas.grid(sticky='ew')
        self.elems = []

    def add_rectangle(self, x, y, width, height, **kwargs):
        r = Rectangle(self, x, y, width, height, **kwargs)
        self.elems.append(r)
        return r

    def add_oval(self, x, y, width, height, **kwargs):
        o = Oval(self, x, y, width, height, **kwargs)
        self.elems.append(o)
        return o

    def add_text(self, x, y, **kwargs):
        t = Text(self, x, y, **kwargs)
        self.elems.append(t)
        return t
